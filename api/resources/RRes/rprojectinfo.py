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

class RInfoProject(Resource):
    def get(self):
        return {'status':'OK', 'text':'ok'}

    def post(self):
        parser.add_argument('action')
        args = parser.parse_args()
        print(args['action'])

# action=get_infoproject (весь список)
        if args['action'] == 'get_infoproject':
            parser.add_argument('token')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            list = db.session.execute('SELECT '
                                      'project_info.*, '
                                      'projects.name AS project_name, '
                                      'clients.name AS client_name'
                                      ' FROM '
                                      'project_info '
                                      'LEFT JOIN clients ON project_info.id_client = clients.id '
                                      'LEFT JOIN projects ON clients.id = projects.id_orgname '
                                      'LEFT JOIN org_name ON clients.orgname = org_name.id'
                                      ' WHERE '
                                      'org_name.id = :val'
                                      ' AND	NOT project_info.remove', {'val': wor.id_org_name}).all()
            status_list = []
            for c in list:
                d = {}
                d['id'] = c.id
                d['id_project'] = c.id_project
                d['id_client'] = c.id_client
                d['info'] = c.info
                d['date'] = c.date
                d['project_name'] = c.project_name
                d['client_name'] = c.client_name
                status_list.append(d)
            return status_list

# action=get_clients (id проекта в параметрах) (Список всех клиентов выбранного проекта)
        elif args['action'] == 'get_clients':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            list = db.session.execute('SELECT '
                                      'project_info.*, '
                                      'projects.name AS project_name, '
                                      'clients.name AS client_name'
                                      ' FROM '
                                      'project_info '
                                      'LEFT JOIN clients ON project_info.id_client = clients.id '
                                      'LEFT JOIN projects ON clients.id = projects.id_orgname '
                                      'LEFT JOIN org_name ON clients.orgname = org_name.id'
                                      ' WHERE '
                                      'id_client.id = :val'
                                      ' AND	NOT project_info.remove', {'val': args1['id']}).all()
            status_list = []
            for c in list:
                d = {}
                d['id'] = c.id
                d['id_project'] = c.id_project
                d['id_client'] = c.id_client
                d['info'] = c.info
                d['date'] = c.date
                d['project_name'] = c.project_name
                d['client_name'] = c.client_name
                status_list.append(d)
            return status_list


# action=get_projects (id клиента в параметрах) (Список всех проектов выбранного клиента)
        elif args['action'] == 'get_projects':
            parser.add_argument('token')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter(MToken.token == args1['token']).one()
            wor = MWorker.query.filter(MWorker.id == tok.worker_id).one()
            orgname = MOrgName.query.filter(MOrgName.id == wor.id_org_name).one()
            list = db.session.execute('SELECT '
                                      'project_info.*, '
                                      'projects.name AS project_name, '
                                      'clients.name AS client_name'
                                      ' FROM '
                                      'project_info '
                                      'LEFT JOIN clients ON project_info.id_client = clients.id '
                                      'LEFT JOIN projects ON clients.id = projects.id_orgname '
                                      'LEFT JOIN org_name ON clients.orgname = org_name.id'
                                      ' WHERE '
                                      'id_project.id = :val'
                                      ' AND	NOT project_info.remove', {'val': args1['id']}).all()
            status_list = []
            for c in list:
                d = {}
                d['id'] = c.id
                d['id_project'] = c.id_project
                d['id_client'] = c.id_client
                d['info'] = c.info
                d['date'] = c.date
                d['project_name'] = c.project_name
                d['client_name'] = c.client_name
                status_list.append(d)
            return status_list


# action=delete_infoproject
        elif args['action'] == 'delete_infoproject':
            parser.add_argument('token')
            parser.add_argument('id_project')
            parser.add_argument('id_workers')
            parser.add_argument('info')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            uniqu = MProjectInfo.query.filter(MProjectInfo.id_project == args1['id_project']) \
                .filter(MProjectInfo.id_workers == args1['id_workers']).first()
            if hasattr(uniqu, 'id'):
                uniqu.remove = True
                db.session.add(uniqu)
                db.session.commit()
                return {'status': 'true', 'text': uniqu.id}
# action=add_infoproject
        elif args['action'] == 'add_infoproject':
            parser.add_argument('token')
            parser.add_argument('id_project')
            parser.add_argument('id_workers')
            parser.add_argument('info')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            uniqu = MProjectInfo.query.filter(MProjectInfo.id_project == args1['id_project']) \
                .filter(MProjectInfo.id_workers == args1['id_workers']).first()
            if hasattr(uniqu, 'id'):
                if uniqu.remove == True:
                    uniqu.remove = False
                    db.session.add(uniqu)
                    db.session.commit()
                    return {'status': 'true', 'text': uniqu.id}
                else:
                    return {'status': 'false', 'text': uniqu.id}
            else:
                infoproject_add = MProjectInfo.query.filter(id_workers=args1['id_workers'],
                                                            id_project= args1['id_project'],
                                                            info = args1['info'])
                db.session.add(infoproject_add)
                db.session.commit()
                return {'status': 'true', 'text': infoproject_add.id}
# action=edit_infoproject
        elif args['action'] == 'edit_infoproject':
            parser.add_argument('token')
            parser.add_argument('id_project')
            parser.add_argument('id_clients')
            parser.add_argument('info')
            parser.add_argument('id')
            args1 = parser.parse_args()
            tok = MToken.query.filter_by(token=args1['token']).first()
            wor = MWorker.query.filter_by(id=tok.worker_id).one()
            # clientpc = MClientPC.query.filter(MClientPC.name == args1['name'])
            # if hasattr(clientpc, 'name'):
            #    return {'status': 'false', 'text': '102'}
            uniqu = MProjectInfo.query.filter(MProjectInfo.id_project == args1['id_project']) \
                .filter(MProjectInfo.id_client == args1['id_clients']).filter(MProjectInfo.id != args1['id']) \
                .first()
            if hasattr(uniqu, 'id'):
                return {'status': 'false', 'text': '112'}

            mprojectinfo_edit = MProjectInfo.query.filter_by(id=args1['id']).one()
            if hasattr(mprojectinfo_edit, 'id'):
                mprojectinfo_edit.id_project = args1['id_project']
                mprojectinfo_edit.id_client = args1['id_clients']
                mprojectinfo_edit.info = args1['info']
                db.session.add(mprojectinfo_edit)
                db.session.commit()
                return {'status': 'true', 'text': mprojectinfo_edit.id}
            else:
                return {'status': 'false', 'text': '105'}
            return {'status': 'true'}