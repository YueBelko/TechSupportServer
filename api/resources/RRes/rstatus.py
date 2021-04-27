# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import Flask, request, jsonify
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
from api.models.clients import MClients, MContacts, MClientPC, MBlockHistory
from api.models.projects import MProjectRequest,\
    MProject, MRequestStatus, MProjectInfo,\
    MChangeInTheProject, MProjectDoc, MProjectWorkers, MProjectQuestions
from api import db
import datetime

parser = reqparse.RequestParser()

class RStatusRequest(Resource):
    def get(self):
        return {'status':'OK', 'text':'ok'}

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])

        if args['action'] == 'get_status':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            status_list = []
            status = db.session.query(MRequestStatus).filter(MRequestStatus.id_orgname == orgname.id)\
                .filter(MRequestStatus.remove == False)
            for r in status:
                d = {}
                d['status'] = r.status
                d['id'] = r.id
                d['id_orgname'] = r.id_orgname
                d['filter'] = r.filter
                d['remove_in_report'] = r.remove_in_report
                d['remove'] = r.remove

                status_list.append(d)
            return status_list

        elif args['action'] == 'add_status':
            parser.add_argument('token')
            parser.add_argument('status')
            parser.add_argument('filter')
            parser.add_argument('remove_in_report')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            if args1['remove_in_report']:
                remove_in_report=True
            else:
                remove_in_report=False
            status_add = MRequestStatus(status=args1['status'],
                                        filter = int(args1['filter']),
                                        remove_in_report = remove_in_report,
                                        id_orgname = int(orgname.id))
            db.session.add(status_add)
            db.session.commit()
            return {'status': 'true', 'text': status_add.id}

        elif args['action'] == 'edit_status':
            parser.add_argument('id')
            parser.add_argument('token')
            parser.add_argument('status')
            parser.add_argument('filter')
            parser.add_argument('remove_in_report')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            if args1['remove_in_report']:
                remove_in_report=True
            else:
                remove_in_report=False
            status = MRequestStatus.query.filter_by(id=args1['id']).first()
            if not hasattr(status,'id'):
                return {'status': 'false', 'text': '102'}
            status.status = args1['status']
            status.filter = args1['filter']
            status.remove_in_report = remove_in_report
            db.session.add(status)
            db.session.commit()
            return {'status': 'true', 'text':status.id}

        elif args['action'] == 'delete_status':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectstatus = MRequestStatus.query.filter(MClients.orgname == orgname.id)\
                .filter(MRequestStatus.id == args1['id']).one()
            if not hasattr(projectstatus, 'id'):
                return {'status': 'false', 'text': '100'}
            projectstatus.remove = True
            db.session.add(projectstatus)
            db.session.commit()
            return {'status': 'true', 'text': 'project status removed'}

        return {'status': 'false', 'text': '102'}