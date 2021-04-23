# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api.models.projects import MProjectRequest, MProject, MRequestStatus, MProjectInfo, MChangeInTheProject
from api import db
import datetime

parser = reqparse.RequestParser()

class RProject(Resource):
    def get(self):
        return {'status':'OK', 'text':'ok'}

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
        if args['action'] == 'get_project':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            args1 = parser.parse_args()
            print('get_project')
        return {'status':'OK', 'text':'ok'}