# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api import db
import datetime

parser = reqparse.RequestParser()


class RClientpc(Resource):
    def get(self):
        return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_clientpc':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            client = MClients.query.filter_by(id=args1['id_clients'], orgname=wor.id_org_name, remove=False)
            clientpc = MClientPC.query.filter_by(id_clients=args1['id_clients'],remove=False).all()
            clientpc_list = []
            for c in clientpc:
                d = {}
                d['id'] = c.id
                d['id_clients'] = c.id_clients
                d['name'] = c.name
                d['rdesk_soft'] = c.rdesk_soft
                d['rdesk_id'] = c.rdesk_id
                clientpc_list.append(d)
            return clientpc_list
            #return []
        elif args['action'] == 'add_clientpc':
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
        elif args['action'] == 'edit_clientpc':
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
        elif args['action'] == 'delete_clientpc':
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



        return {'status': 'false', 'text': '101'}
