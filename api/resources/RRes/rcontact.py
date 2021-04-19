# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api import db
import datetime

parser = reqparse.RequestParser()


class RContact(Resource):
    def get(self):
        return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_contacts':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            client = MClients.query.filter_by(id=args1['id_clients'], orgname=wor.id_org_name, remove=False)
            contact = MContacts.query.filter_by(id_clients=args1['id_clients'],remove=False).all()
            contacts_list = []
            for c in contact:
                d = {}
                d['id'] = c.id
                d['id_clients'] = c.id_clients
                d['fio'] = c.fio
                d['phone'] = c.phone
                d['email'] = c.email
                d['position'] = c.position
                contacts_list.append(d)
            return contacts_list
            #return []
        elif args['action'] == 'add_contacts':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            parser.add_argument('fio')
            parser.add_argument('phone')
            parser.add_argument('position')
            parser.add_argument('email')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            contact = MContacts.query.filter(MContacts == args1['fio'])
            if hasattr(contact, 'fio'):
                return {'status': 'false', 'text': '102'}

            contact_add = MContacts(id_clients=args1['id_clients'],
                                  fio=args1['fio'],
                                  phone=args1['phone'],
                                  position=args1['position'],
                                  email=args1['email'])
            db.session.add(contact_add)
            db.session.commit()
            return {'status': 'true', 'text': 'contact added'}
        elif args['action'] == 'edit_contacts':
            parser.add_argument('token')
            parser.add_argument('fio')
            parser.add_argument('position')
            parser.add_argument('phone')
            parser.add_argument('email')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            contact = MContacts.query.filter_by(id=args1['id']).first()

            if hasattr(contact, 'fio'):
                contact.fio = args1['fio']
                contact.position = args1['position'],
                contact.phone = args1['phone'],
                contact.email = args1['email'],
                db.session.add(contact)
                db.session.commit()
                return {'status': 'true', 'text': 'contact edited '}
            else:
                return {'status': 'error', 'text':'100'}
        elif args['action'] == 'delete_contacts':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            contact = MContacts.query.filter(MClients.id == args1['id']).first()
            print(contact.id)
            if hasattr(contact, 'id'):
                contact.remove = True
                db.session.add(contact)
                db.session.commit()
                return {'status': 'true', 'text': 'contact removed '}
            else:
                return {'status': 'error', 'text':'100'}


        return {'status': 'false', 'text': '101'}
