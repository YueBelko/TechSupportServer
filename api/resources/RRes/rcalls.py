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
                calls = db.session.query(MCall.id,
                                         MCall.id_clients,
                                         MCall.id_worker,
                                         MCall.time_in,
                                         MCall.time_out,
                                         MCall.reason_calls,
                                         MCall.id_project,
                                         MCall.id_clients_contact,
                                         MCall.call_ended,
                                         MCall.remove,
                                         MWorker.fio.label('worker_fio'),
                                         MWorker.id.label('worker_id'),
                                         MClients.name.label('client_name'),
                                         MClients.unp.label('client_unp'),
                                         MContacts.id.label('contact_id'),
                                         MContacts.fio.label('contact_fio')) \
                    .join(MWorker, MWorker.id == MCall.id_worker) \
                    .join(MOrgName, MWorker.id_org_name == MOrgName.id) \
                    .join(MClients, MCall.id_clients == MClients.id) \
                    .join(MContacts, MClients.id == MContacts.id_clients) \
                    .filter(MWorker.id_org_name == wor.id_org_name) \
                    .all()
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
            parser.add_argument('id_clients')
            parser.add_argument('name')
            parser.add_argument('rdesk_soft')
            parser.add_argument('rdesk_id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            print(args1['name'])
            #clientpc = MClientPC.query.filter(MClientPC.name == args1['name'])
            #if hasattr(clientpc, 'name'):
            #    return {'status': 'false', 'text': '102'}

            clientpc_add = MClientPC(id_clients=args1['id_clients'],
                                  name=args1['name'],
                                  rdesk_soft=args1['rdesk_soft'],
                                  rdesk_id=args1['rdesk_id'])
            db.session.add(clientpc_add)
            db.session.commit()
            return {'status': 'true', 'text': 'clientpc added'}
        elif args['action'] == 'edit_call':
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('rdesk_soft')
            parser.add_argument('rdesk_id')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            clientpc = MClientPC.query.filter_by(id=args1['id']).first()

            if hasattr(clientpc, 'name'):
                clientpc.name = args1['name']
                clientpc.rdesk_soft = args1['rdesk_soft'],
                clientpc.rdesk_id = args1['rdesk_id'],
                db.session.add(clientpc)
                db.session.commit()
                return {'status': 'true', 'text': 'clientpc edited '}
            else:
                return {'status': 'error', 'text':'100'}
        elif args['action'] == 'delete_call':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            clientpc = MClientPC.query.filter(MClientPC.id == args1['id']).first()
            print(clientpc.id)
            if hasattr(clientpc, 'id'):
                clientpc.remove = True
                db.session.add(clientpc)
                db.session.commit()
                return {'status': 'true', 'text': 'clientpc removed '}
            else:
                return {'status': 'error', 'text':'100'}

        elif args['action'] == 'get_reason':
            reason_list = []
            reason = db.session.query(MCall.reason_calls).group_by(MCall.reason_calls).all()
            for r in reason:
                d = {}
                d['reason_calls'] = r.reason_calls
                reason_list.append(d)
            return reason_list



        return {'status': 'false', 'text': '101'}
