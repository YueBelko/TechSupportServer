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

class RSubversion(Resource):
    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'add_subversion':
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('phone')
            parser.add_argument('city')
            parser.add_argument('sub_cheff')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            sub_t = MSubdivision.query.filter_by(name=args1['name'],org_name=wor.id_org_name).first()
            if hasattr(sub_t, 'name'):
                return {'status': 'false', 'text': '102'}

            if tok.workers_id.admin:
                t = MSubdivision.query.filter_by(name=args1['name'])
                if not hasattr(t,'id') :
                    sub_add = MSubdivision(name=args1['name'],
                                           sub_cheff=args1['sub_cheff'],
                                           phone=args1['phone'],
                                           city=args1['city'],
                                           org_name=wor.id_org_name)
                    db.session.add(sub_add)
                    db.session.commit()
                    return {'status': 'true'}
                else:
                    return {'status': 'true', 'text': '103'}


            return {'status': 'false', 'text': '104'}
        elif args['action'] == 'edit_subversion':
            parser.add_argument('id')
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('phone')
            parser.add_argument('city')
            parser.add_argument('sub_cheff')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            if hasattr(tok,'id') and hasattr(tok, 'worker_id'):
                wor1 = MWorker.query.get(tok.worker_id)
                sub_t = MSubdivision.query.filter_by(name=args1['name'], org_name=wor1.id_org_name).first()
                if tok.workers_id.admin:
                    t = MSubdivision.query.get(args1['id'])
                    if hasattr(t, 'id'):
                        t.name=args1['name']
                        t.sub_cheff=args1['sub_cheff']
                        t.phone=args1['phone']
                        t.city=args1['city']
                        t.org_name=wor1.id_org_name
                        db.session.add(t)
                        db.session.commit()
                        return {'status': 'true'}
                    else:
                        return {'status': 'true', 'text': '105'}

                return {'status': 'false', 'text': '106'}
        elif args['action'] == 'delete_subversion':
            print('Delete OK!!!')
            parser.add_argument('id')
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            sub_t = MSubdivision.query.filter_by(id=args1['id'], org_name=wor.id_org_name).first()
            if not hasattr(sub_t, 'name'):
                return {'status': 'false', 'text': '107'}

            if tok.workers_id.admin:
                if hasattr(sub_t, 'id'):
                    sub_t.remove = True
                    db.session.add(sub_t)
                    db.session.commit()
                    return {'status': 'true'}

                return {'status': 'true', 'text': '108'}

            return {'status': 'false', 'text': '109'}
        elif args['action'] == 'get_subversion':
            parser.add_argument('token')
            args1 = parser.parse_args()
            if its_admin(args1['token']):
                tok = MToken.query.filter_by(token=args1['token']).first()
                wor = MWorker.query.filter_by(id=tok.worker_id).one()
                sub = MSubdivision.query.filter_by(org_name=wor.id_org_name,remove=False).all()
                lst = []
                for w in sub:
                    d = {}
                    d['id'] = w.id
                    d['name'] = w.name
                    d['sub_cheff'] = w.sub_cheff
                    d['phone'] = w.phone
                    d['city'] = w.city
                    d['org_name'] = w.orgname_id.id
                    d['org_name_name'] = w.orgname_id.name
                    lst.append(d)
                return lst
            return []

        return {'status': 'false', 'text': '111'}

