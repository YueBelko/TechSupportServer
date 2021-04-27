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

class RProject(Resource):
    def get(self):
        return {'status':'OK', 'text':'ok'}

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])
### GET DATA OF DATABASE

        if args['action'] == 'get_project':
            parser.add_argument('token')
            parser.add_argument('id_clients')
            args1 = parser.parse_args()

            return {'status':'ok'}
### ADD
### EDIT
### DELETE
        elif args['action'] == 'del_project':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            project = MProject.query.filter(MClients.orgname == orgname.id).filter(MProject.id == args1['id']).one()
            if not hasattr(project, 'id'):
                return {'status': 'error', 'text': '100'}
            project.remove = True
            db.session.add(project)
            db.session.commit()
            return {'status': 'ok', 'text': 'project removed'}
        elif args['action'] == 'del_project_doc':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectdoc = MProjectDoc.query.filter(MClients.orgname == orgname.id)\
                .filter(MProjectDoc.id == args1['id']).one()
            if not hasattr(projectdoc, 'id'):
                return {'status': 'error', 'text': '100'}
            projectdoc.remove = True
            db.session.add(projectdoc)
            db.session.commit()
            return {'status': 'ok', 'text': 'project removed'}
        elif args['action'] == 'del_project_change':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectchange = MChangeInTheProject.query.filter(MClients.orgname == orgname.id)\
                .filter(MChangeInTheProject.id == args1['id']).one()
            if not hasattr(projectchange, 'id'):
                return {'status': 'error', 'text': '100'}
            projectchange.remove = True
            db.session.add(projectchange)
            db.session.commit()
            return {'status': 'ok', 'text': 'project change removed'}
        elif args['action'] == 'del_project_info':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectinfo = MProjectInfo.query.filter(MClients.orgname == orgname.id)\
                .filter(MProjectInfo.id == args1['id']).one()
            if not hasattr(projectinfo, 'id'):
                return {'status': 'error', 'text': '100'}
            projectinfo.remove = True
            db.session.add(projectinfo)
            db.session.commit()
            return {'status': 'ok', 'text': 'project info removed'}
        elif args['action'] == 'del_project_request':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectrequest = MProjectRequest.query.filter(MClients.orgname == orgname.id)\
                .filter(MProjectRequest.id == args1['id']).one()
            if not hasattr(projectrequest, 'id'):
                return {'status': 'error', 'text': '100'}
            projectrequest.remove = True
            db.session.add(projectrequest)
            db.session.commit()
            return {'status': 'ok', 'text': 'project request removed'}
        elif args['action'] == 'del_project_workers':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectworkers = MProjectWorkers.query.filter(MClients.orgname == orgname.id)\
                .filter(MProjectWorkers.id == args1['id']).one()
            if not hasattr(projectworkers, 'id'):
                return {'status': 'error', 'text': '100'}
            projectworkers.remove = True
            db.session.add(projectworkers)
            db.session.commit()
            return {'status': 'ok', 'text': 'project workers removed'}
        elif args['action'] == 'del_project_workers':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectquestions = MProjectQuestions.query.filter(MClients.orgname == orgname.id)\
                .filter(MProjectQuestions.id == args1['id']).one()
            if not hasattr(projectquestions, 'id'):
                return {'status': 'error', 'text': '100'}
            projectquestions.remove = True
            db.session.add(projectquestions)
            db.session.commit()
            return {'status': 'ok', 'text': 'project questions removed'}


### GET LIST
        elif args['action'] == 'get_status':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            status_list = []
            status = db.session.query(MRequestStatus.status).filter(MRequestStatus.id_orgname == orgname.id).group_by(MRequestStatus.status)
            for r in status:
                d = {}
                d['reason_calls'] = r.reason_calls
                status_list.append(d)
            return status_list

        return {'status':'ERROR', 'text':'102'}

