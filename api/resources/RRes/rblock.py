# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api import db
import datetime

parser = reqparse.RequestParser()


class RBlock(Resource):
    def get(self):
        return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_blocklist':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            client = MClients.query.filter_by(id=args1['id_clients'], orgname=wor.id_org_name, remove=False)
            block = MBlockHistory.query.filter_by(id_clients=args1['id_clients']).all()
            block_list = []
            for c in block:
                d = {}
                d['id'] = c.id
                d['id_clients'] = c.id_clients
                d['data_block'] = str(c.data_block)
                d['blocking_reason'] = c.blocking_reason
                d['status'] = str(c.status)
                d['remove'] = str(c.remove)
                block_list.append(d)
            return block_list
        elif args['action'] == 'block':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            parser.add_argument('blocking_reason')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            client = MClients.query.filter_by(id=args1['id_clients']).one()
            client.block = True
            client.blocking_reason = args1['blocking_reason']
            db.session.add(client)
            db.session.commit()
            block_add = MBlockHistory(id_clients=args1['id_clients'],
                                     blocking_reason=args1['blocking_reason'],
                                     status=True)
            db.session.add(block_add)
            db.session.add(client)
            db.session.commit()
            return {'status': 'true', 'text': 'clientpc added'}
        elif args['action'] == 'unblock':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            parser.add_argument('blocking_reason')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            client = MClients.query.filter_by(id=args1['id_clients']).one()

            client.block = False
            client.blocking_reason = args1['blocking_reason']
            db.session.add(client)
            db.session.commit()
            block_add = MBlockHistory(id_clients=args1['id_clients'],
                                     blocking_reason=args1['blocking_reason'],
                                     status=False)
            db.session.add(block_add)
            db.session.commit()
            return {'status': 'true', 'text': 'clientpc added'}

        return {'status': 'false', 'text': '101'}