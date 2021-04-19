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


class ROrgName(Resource):

    def get(self):

        return {'Status': 'ok'}

    def post(self):
        parser.add_argument('code')
        args = parser.parse_args()
        code = args['code']
        worker = MOrgName.query.filter_by(code=code).first()
        if hasattr(worker, 'name'):
            return {'status': 'true', 'name': worker.name, 'code': worker.code, 'ID': worker.id}
        else:
            return { 'status' : 'false', 'name' : 'Ты тупой', 'code' : '', 'ID': ''}

