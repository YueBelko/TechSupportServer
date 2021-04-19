# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api import db
import secrets
import hashlib
import json
from api.resources.func import normal, its_admin, get_orgname

parser = reqparse.RequestParser()

class RWorkers(Resource):

    def get(self):
        return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'authorization':
            parser.add_argument('login')
            parser.add_argument('password')
            parser.add_argument('info')
            parser.add_argument('org')
            args1 = parser.parse_args()
            code = args1['org']
            login = normal(args1['login'])
            org = MOrgName.query.filter_by(code=code).first()
            wor = MWorker.query.filter_by(login=login).first()
            if hasattr(org, 'code') and hasattr(wor, 'login') and hasattr(wor, 'password'):

                if wor.login == login and wor.password == args1['password'] and org.id == wor.id_org_name:
                    token_in = secrets.token_hex(25)
                    token = MToken(token=token_in, name='test', worker_id=wor.id, sys_info=args1['info'], remove=False)
                    db.session.add(token)
                    db.session.commit()
                    return {'status': 'true',
                            'fio': wor.fio,
                            'admin': wor.admin,
                            'subversion': wor.id_subversion,
                            'token': token_in}
            else:
                return {'status':'false', 'fio':'', 'subversion':'', 'token': ''}
        elif args['action'] == 'token_verification':
            parser.add_argument('token')
            parser.add_argument('info')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            if hasattr(tok,'token') and tok.sys_info == args1['info']:
                wor = MWorker.query.filter_by(id=tok.worker_id).first()
                return {'status': 'true',
                        'fio': wor.fio,
                        'admin': wor.admin,
                        'subversion': wor.id_subversion,
                        'token': tok.token}
        elif args['action'] == 'worker_verification':
            parser.add_argument('token')
            parser.add_argument('login')
            parser.add_argument('password')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).first()
            if hasattr(tok, 'token')\
                    and hasattr(wor, 'login')\
                    and hasattr(wor,'password')\
                    and normal(args1['login']) == wor.login\
                    and args1['password'] == wor.password\
                    and wor.remove == False:
                return {'status': 'true', 'text': 'ok'}
            else:
                return {'status': 'false', 'text': '101'}
        elif args['action'] == 'add_worker':
            parser.add_argument('login')
            parser.add_argument('password')
            parser.add_argument('token')
            parser.add_argument('fio')
            parser.add_argument('work_phone')
            parser.add_argument('id_subversion')
            parser.add_argument('admin')
            args1 = parser.parse_args()
            wor_t = MWorker.query.filter_by(login=normal(args1['login'])).first()
            if hasattr(wor_t, 'login'):
                return {'status': 'false', 'text': '102'}
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            admin = args1['admin']
            if admin == 'True':
                admin = True
            else:
                admin = False
            if hasattr(tok,'token'):
                wor_add = MWorker(login=normal(args1['login']),
                                  password=args1['password'],
                                  fio=args1['fio'],
                                  work_phone=args1['work_phone'],
                                  id_org_name=wor.id_org_name,
                                  id_subversion=args1['id_subversion'],
                                  admin=admin)
                db.session.add(wor_add)
                db.session.commit()
                return {'status': 'true'}
        elif args['action'] == 'get_workers':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).first()
            if hasattr(tok, 'token') and hasattr(wor,'id') and wor.admin:
                workers = MWorker.query.filter(MWorker.id_org_name == wor.id_org_name, MWorker.remove == False).all()
                lst = []
                for w in workers:
                    d = {}
                    d['id'] = w.id
                    d['login'] = w.login
                    d['fio'] = w.fio
                    d['work_phone'] =w.work_phone
                    d['admin'] = str(w.admin)
                    d['id_org_name'] = w.orgname_id.id
                    d['id_org_fulname'] = w.orgname_id.name
                    d['id_subversion'] = w.subversion_orgname.id
                    d['id_subversion_name'] = w.subversion_orgname.name
                    lst.append(d)
                return lst
            else:
                return []

        elif args['action'] == 'edit_worker':
            parser.add_argument('token')
            parser.add_argument('id')
            parser.add_argument('password')
            parser.add_argument('fio')
            parser.add_argument('work_phone')
            parser.add_argument('id_subversion')
            parser.add_argument('admin')
            args1 = parser.parse_args()
            wor = MWorker.query.filter_by(id=args1['id']).first()
            if hasattr(wor,'id') == False:
                return {'status': 'false', 'text': '103'}
            tok = MToken.query.filter_by(token=args1['token']).first()

            if hasattr(tok,'id') and hasattr(tok, 'worker_id'):
                wor1 = MWorker.query.get(tok.worker_id)
                if wor1.admin == False:
                    return {'status': 'false', 'text': '103'}
                wor_upd = MWorker.query.get(args1['id'])
                wor_upd.password = args1['password']
                wor_upd.fio = args1['fio']
                wor_upd.work_phone = args1['work_phone']
                wor_upd.id_subversion = args1['id_subversion']
                if args1['admin'] == 'True':
                    wor_upd.admin = True
                else:
                    wor_upd.admin = False
                db.session.add(wor_upd)
                db.session.commit()
            return {'status': 'true'}
        elif args['action'] == 'delete_worker':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            wor = MWorker.query.filter_by(id=args1['id']).first()
            if hasattr(wor, 'id') == False:
                return {'status': 'false', 'text': '103'}
            tok = MToken.query.filter_by(token=args1['token']).first()
            if hasattr(tok, 'id') and hasattr(tok, 'worker_id'):
                wor1 = MWorker.query.get(tok.worker_id)
                if wor1.admin:
                    wor_upd = MWorker.query.get(args1['id'])
                    wor_upd.remove = True
                    db.session.add(wor_upd)
                    db.session.commit()
                    return {'status': 'true'}
                return {'status': 'false', 'text': '103'}

        return {'status': 'false'}
