# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api import db
import datetime
import secrets
import hashlib
import json
from api.resources.func import normal, its_admin, get_orgname

parser = reqparse.RequestParser()


class RClients(Resource):
    def get(self):
        return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_clients':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            clients = MClients.query.filter_by(orgname=wor.id_org_name,remove=False).all()
            client_list = []
            for c in clients:
                d = {}
                d['id'] = c.id
                d['name'] = c.name
                d['unp'] = c.unp
                d['phone'] = c.phone
                d['u_address'] = c.u_address
                d['email'] = c.email
                d['block'] = str(c.block)
                d['blocking_reason'] = c.blocking_reason
                d['orgname'] = c.orgname
                d['support_time'] = c.support_time
                d['support_time_string'] = str(datetime.timedelta(seconds=c.support_time))
                client_list.append(d)
            return client_list
            #return []
        elif args['action'] == 'add_clients':
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('unp')
            parser.add_argument('phone')
            parser.add_argument('u_address')
            parser.add_argument('email')
            parser.add_argument('support_time')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            client = MClients.query.filter(MClients.name == args1['name'])
            if hasattr(client, 'name'):
                return {'status': 'false', 'text': '102'}

            client_add = MClients(name=args1['name'],
                                  unp=args1['unp'],
                                  phone=args1['phone'],
                                  u_address=args1['u_address'],
                                  email=args1['email'],
                                  support_time=args1['support_time'],
                                  orgname=wor.id_org_name)
            db.session.add(client_add)
            db.session.commit()
            return {'status': 'true', 'text': 'client added'}
        elif args['action'] == 'edit_clients':
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('unp')
            parser.add_argument('phone')
            parser.add_argument('u_address')
            parser.add_argument('email')
            parser.add_argument('id')
            parser.add_argument('support_time')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            client = MClients.query.filter_by(id=args1['id']).first()

            if hasattr(client, 'id'):
                client.name=args1['name']
                client.unp=args1['unp'],
                client.phone=args1['phone'],
                client.u_address=args1['u_address'],
                client.email=args1['email'],
                client.support_time=args1['support_time']
                client.orgname=wor.id_org_name
                db.session.add(client)
                db.session.commit()
                return {'status': 'true', 'text': 'client edited '}
            else:
                return {'status': 'false', 'text':'100'}
        elif args['action'] == 'delete_clients':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            client = MClients.query.filter(MClients.id == args1['id']).first()
            if hasattr(client, 'id'):
                client.remove = True
                db.session.add(client)
                db.session.commit()
                return {'status': 'true', 'text': 'client removed '}
            else:
                return {'status': 'error', 'text':'100'}


        return {'status': 'false', 'text': '101'}

