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
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            project = db.session.execute('SELECT '
                                         'projects.*, '
                                         'request_status.status AS status_text, '
                                         'org_name.name AS org_name'
                                         ' FROM '
                                         'projects '
                                         'LEFT JOIN org_name ON projects.id_orgname = org_name.id '
                                         'LEFT JOIN request_status ON projects.status = request_status.id '
                                         ' WHERE '
                                         'NOT projects.remove AND '
                                         'projects.id_orgname = :val', {'val': wor.id_org_name}).all()
            project_list = []
            for c in project:
                d = {}
                d['id'] = c.id
                d['id_orgname'] = c.id_orgname
                d['name'] = c.name
                d['status'] = c.status
                d['status_text'] = c.status_text
                d['org_name'] = c.org_name
                project_list.append(d)

            return project_list
### ADD
        elif args['action'] == 'add_project':
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('status')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            # clientpc = MClientPC.query.filter(MClientPC.name == args1['name'])
            # if hasattr(clientpc, 'name'):
            #    return {'status': 'false', 'text': '102'}

            project_add = MProject(id_orgname=wor.id_org_name,
                                   name = args1['name'],
                                   status = args1['status'])

            db.session.add(project_add)
            db.session.commit()
            return {'status': 'true', 'text': project_add.id}
### EDIT
        elif args['action'] == 'edit_project':
            parser.add_argument('token')
            parser.add_argument('name')
            parser.add_argument('status')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            # clientpc = MClientPC.query.filter(MClientPC.name == args1['name'])
            # if hasattr(clientpc, 'name'):
            #    return {'status': 'false', 'text': '102'}

            project_edit = MProject.query.filter_by(id=args1['id']).first()
            if hasattr(project_edit, 'id'):
                project_edit.name = args1['name']
                project_edit.status = args1['status']
                db.session.add(project_edit)
                db.session.commit()
                return {'status': 'true', 'text': project_edit.id}
            else:
                return {'status': 'false', 'text': '105'}
            return {'status': 'false', 'text': '101'}
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
                return {'status': 'false', 'text': '100'}
            project.remove = True
            db.session.add(project)
            db.session.commit()
            return {'status': 'true', 'text': 'project removed'}
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

        elif args['action'] == 'del_project_questions':
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

