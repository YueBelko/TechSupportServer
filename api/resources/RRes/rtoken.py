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

class RToken(Resource):
    def get(self):
        return {'Status': 'OK'}, 201

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_token':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            if hasattr(tok,'id'):
                wor = MWorker.query.get(tok.worker_id)
                list = MToken.query.filter(MToken.worker_id == wor.id).all()
                lst = []
                for w in list:
                    d = {}
                    d['id'] = w.id
                    d['token'] = w.token
                    d['name'] = w.name
                    d['sys_info'] = w.sys_info
                    lst.append(d)
                return lst

            return []
        elif args['action'] == 'delete_token':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).first()
            tok_del = MToken.query.filter(MToken.id == args1['id'],MToken.worker_id == wor.id).first()
            db.session.delete(tok_del)
            db.session.commit()
            return {'status':'true','text':'ok'}
        return {'status': 'false', 'text':'113'}