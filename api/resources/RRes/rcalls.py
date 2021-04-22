# -*- coding: utf-8 -*-
from api import db
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api.models.calls import MCall
from pprint import pprint
import datetime

parser = reqparse.RequestParser()


class RCall(Resource):
    def get(self):
       return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_calls':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            if wor.admin:
                calls = db.session.execute('SELECT calls.*,	'
                                           'contacts.fio AS contact_fio, '
                                           'contacts.id AS contact_id, '
                                           'worker.id AS worker_id, '
                                           'worker.fio AS worker_fio, '
                                           'COALESCE(clients.unp,\'\''') AS client_unp, '
                                           'clients.id AS client_id, '
                                           'COALESCE(clients.name,\'\''') AS client_name '
                                           'FROM'
                                           ' calls '
                                           'LEFT JOIN worker ON calls.id_worker = worker.id '
                                           'LEFT JOIN clients ON calls.id_clients = clients.id '
                                           'LEFT JOIN contacts ON calls.id_clients_contact = contacts.id '
                                           'WHERE '
                                           'NOT calls.remove AND '
                                           'worker.id_org_name = :val', {'val': wor.id_org_name}).all()
            else:
                calls = db.session.execute('SELECT calls.*,	'
                                           'contacts.fio AS contact_fio, '
                                           'contacts.id AS contact_id, '
                                           'worker.id AS worker_id, '
                                           'worker.fio AS worker_fio, '
                                           'COALESCE(clients.unp,\'\''') AS client_unp, '
                                           'clients.id AS client_id, '
                                           'COALESCE(clients.name,\'\''') AS client_name '
                                           'FROM'
                                           ' calls '
                                           'LEFT JOIN worker ON calls.id_worker = worker.id '
                                           'LEFT JOIN clients ON calls.id_clients = clients.id '
                                           'LEFT JOIN contacts ON calls.id_clients_contact = contacts.id '
                                           'WHERE '
                                           'NOT calls.remove AND '
                                           'calls.id_worker = :val', {'val':wor.id}).all()
            calls_list = []
            for c in calls:
                d = {}
                d['id'] = c.id
                d['id_clients'] = c.id_clients
                d['id_clients_name'] = c.client_name + ' ' + c.client_unp
                d['id_worker'] = c.worker_id
                d['id_worker_name'] = c.worker_fio
                d['time_in'] = str(c.time_in)
                d['time_out'] = str(c.time_out)
                d['time'] = str(c.time_out - c.time_in)
                d['reason_calls'] = c.reason_calls
                d['id_project'] = c.id_project
                d['id_contacts_call'] = c.contact_id
                d['id_contacts_call_name'] = c.contact_fio
                d['call_ended'] = str(c.call_ended)
                calls_list.append(d)

            return calls_list
            #return []
        elif args['action'] == 'add_call':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            #clientpc = MClientPC.query.filter(MClientPC.name == args1['name'])
            #if hasattr(clientpc, 'name'):
            #    return {'status': 'false', 'text': '102'}

            calls_add = MCall(id_worker=wor.id)
            db.session.add(calls_add)
            db.session.commit()
            return {'status': 'true', 'text': calls_add.id}
        elif args['action'] == 'edit_call':
            parser.add_argument('token')
            parser.add_argument('id')
            parser.add_argument('id_clients')
            parser.add_argument('time_in')
            parser.add_argument('time_out')
            parser.add_argument('reason_calls')
            parser.add_argument('id_project')
            parser.add_argument('id_clients_contact')
            parser.add_argument('call_ended')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            call = MCall.query.filter_by(id=args1['id']).first()
            if hasattr(call, 'id'):
                call.id_clients = args1['id_clients']
                call.time_in = args1['time_in']
                call.time_out = args1['time_out']
                call.reason_calls = args1['reason_calls']
                call.id_project = args1['id_project']
                call.id_clients_contact = args1['id_clients_contact']
                if args1['call_ended'] == 'True':
                    call.call_ended = True
                else:
                    call.call_ended = False
                db.session.add(call)
                db.session.commit()
                return {'status': 'true', 'text': 'call edited '}
            else:
                return {'status': 'error', 'text':'100'}
        elif args['action'] == 'delete_call':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            calls = MCall.query.filter(MCall.id == args1['id']).first()
            if hasattr(calls, 'id'):
                calls.remove = True
                db.session.add(calls)
                db.session.commit()
                return {'status': 'true', 'text': 'clientpc removed '}
            else:
                return {'status': 'error', 'text':'100'}

        elif args['action'] == 'get_reason':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            reason_list = []
            reason = db.session.query(MCall.reason_calls).join(MClients, MClients.id == MCall.id_clients).filter(MClients.orgname == orgname.id).group_by(MCall.reason_calls)
            for r in reason:
                d = {}
                d['reason_calls'] = r.reason_calls
                reason_list.append(d)
            return reason_list



        return {'status': 'false', 'text': '101'}
