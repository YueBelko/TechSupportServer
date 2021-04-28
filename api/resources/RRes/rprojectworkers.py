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

class RProjectWorkers(Resource):
    def get(self):
        return {'status':'OK', 'text':'ok'}

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])

### GET DATA OF DATABASE
        if args['action'] == 'get_projectworkers':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            list = db.session.execute('SELECT '
                                      'worker.id_org_name, '
                                      'worker.fio, '
                                      'projects.name,'
                                      'project_workers.*'
                                      ' FROM '
                                      'project_workers '
                                      'LEFT JOIN worker	ON project_workers.id_workers = worker.id'
                                      'LEFT JOIN projects ON project_workers.id_project = projects.id'
                                      ' WHERE '
                                      'worker.id_org_name = :val'
                                      ' AND	NOT project_workers.remove', {'val': wor.id_org_name}).all()
            status_list = []
            for c in list:
                d = {}
                d['id'] = c.id
                d['name'] = c.name
                d['fio'] = c.fio
                d['id_org_name'] = c.id_org_name
                d['id_project'] = c.id_project
                d['id_workers'] = c.id_workers
                status_list.append(d)
            return status_list
### GET get_workers
        elif args['action'] == 'get_workers':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            workers = db.session.execute('SELECT '
                                         'projects.name,'
                                         'worker.fio, '
                                         'project_workers.*'
                                         ' FROM '
                                         'project_workers '
                                         'LEFT JOIN worker ON project_workers.id_workers = worker.id '
                                         'LEFT JOIN projects ON project_workers.id_project = projects.id'
                                         ' WHERE '
                                         'NOT project_workers.remove AND '
                                         'project_workers.id_workers = :val',{'val': args1['id']}).all()
            workers_list = []
            for c in workers:
                d = {}
                d['id'] = c.id
                d['name'] = c.name
                d['fio'] = c.fio
                d['id_project'] = c.id_project
                d['id_workers'] = c.id_workers
                workers_list.append(d)
            return workers_list

### GET get_projects
        elif args['action'] == 'get_projects':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            project = db.session.execute('SELECT '
                                         'projects.name,'
                                         'worker.fio, '
                                         'project_workers.*'
                                         ' FROM '
                                         'project_workers '
                                         'LEFT JOIN worker ON project_workers.id_workers = worker.id '
                                         'LEFT JOIN projects ON project_workers.id_project = projects.id'
                                         ' WHERE '
                                         'NOT project_workers.remove AND '
                                         'project_workers.id_workers = :val', {'val': args1['id']}).all()
            project_list = []
            for c in project:
                d = {}
                d['id'] = c.id
                d['name'] = c.name
                d['fio'] = c.fio
                d['id_project'] = c.id_project
                d['id_workers'] = c.id_workers
                project_list.append(d)
            return project_list
### ADD DATA
        elif args['action'] == 'add_projectworkers':
            parser.add_argument('token')
            parser.add_argument('id_project')
            parser.add_argument('id_workers')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            uniqu = MProjectWorkers.query.filter(MProjectWorkers.id_project == args1['id_project'])\
                .filter(MProjectWorkers.id_workers == args1['id_workers']).first()
            if hasattr(uniqu,'id'):
                if hasattr(uniqu, 'id'):
                    if uniqu.remove == True:
                        uniqu.remove = False
                        db.session.add(uniqu)
                        db.session.commit()
                        return {'status': 'true', 'text': uniqu.id}
                    else:
                        return {'status': 'false', 'text': uniqu.id}
            else:
                projectworkers_add = MProjectWorkers(id_workers=args1['id_workers'],
                                                     id_project= args1['id_project'])
                db.session.add(projectworkers_add)
                db.session.commit()
                return {'status':'true', 'text':projectworkers_add.id}
### EDIT DATA
        elif args['action'] == 'edit_projectworkers':
            parser.add_argument('token')
            parser.add_argument('id_project')
            parser.add_argument('id_workers')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            # clientpc = MClientPC.query.filter(MClientPC.name == args1['name'])
            # if hasattr(clientpc, 'name'):
            #    return {'status': 'false', 'text': '102'}
            uniqu = MProjectWorkers.query.filter(MProjectWorkers.id_project == args1['id_project']) \
                .filter(MProjectWorkers.id_workers == args1['id_workers']).first()
            if hasattr(uniqu, 'id'):
                return {'status': 'false', 'text': '112'}

            projectworkers_edit = MProjectWorkers.query.filter_by(id=args1['id']).one()
            if hasattr(projectworkers_edit, 'id'):
                projectworkers_edit.id_project = args1['id_project']
                projectworkers_edit.id_workers = args1['id_workers']
                db.session.add(projectworkers_edit)
                db.session.commit()
                return {'status': 'true', 'text': projectworkers_edit.id}
            else:
                return {'status': 'false', 'text': '105'}
            return {'status': 'false', 'text': '101'}

### DELETE DATA OF DATABASE
        elif args['action'] == 'delete_projectworkers':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            projectworkers = MProjectWorkers.query.filter(MProjectWorkers.id == args1['id']).one()
            if hasattr(projectworkers, 'id'):
                projectworkers.remove = True
                db.session.add(projectworkers)
                db.session.commit()
                return {'status': 'true', 'text': 'project workers removed'}
            else:
                return {'status': 'false', 'text': 'not found project'}

### END
        return {'status':'false', 'text':'102'}