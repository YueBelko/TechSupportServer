# -*- coding: utf-8 -*-
from api import db
from datetime import datetime
from sqlalchemy.sql import func
from api.models.clients import MClients


class MProject(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    id_orgname = db.Column(db.Integer(), db.ForeignKey('org_name.id'))
    name = db.Column(db.String(), default='базовый проект')
    status = db.Column(db.Integer(), db.ForeignKey('request_status.id'))
    remove = db.Column(db.Boolean(), default=False)
    id_changeintheproject = db.relationship('MChangeInTheProject', backref='id_changeintheproject', lazy='dynamic')
    id_projectinfo = db.relationship('MProjectInfo', backref='id_projectinfo', lazy='dynamic')

    def __repr__(self):
        return self.id


class MChangeInTheProject(db.Model):
    __tablename__ = 'change_in_the_project'
    id = db.Column(db.Integer(), primary_key=True)
    id_project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    changes = db.Column(db.Text)
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


class MProjectInfo(db.Model):
    __tablename__ = 'project_info'
    id = db.Column(db.Integer(), primary_key=True)
    id_project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    id_client = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    info = db.Column(db.Text(), default='базовая информация о проекте')
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


class MProjectRequest(db.Model):
    __tablename__ = 'project_request'
    id = db.Column(db.Integer(), primary_key=True)
    id_project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    id_worker_created  = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    id_worker_responsible  = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    id_contacts = db.Column(db.Integer(), db.ForeignKey('contacts.id'))
    status = db.Column(db.Integer(), db.ForeignKey('request_status.id'))
    info = db.Column(db.Text(), default='базовая информация о заявке')
    date = db.Column(db.DateTime(), default=datetime.utcnow())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id

class MRequestStatus(db.Model):
    __tablename__ = 'request_status'
    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String(), default='New')
    filter = db.Column(db.Integer(), default='0')
    remove_in_report = db.Column(db.Boolean(), default=False)
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


class ProjectWorkers(db.Model):
    __tablename__ = 'project_workers'
    id = db.Column(db.Integer(), primary_key=True)
    id_project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    id_workers = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


class ProjectDoc(db.Model):
    __tablename__ = 'project_doc'
    id = db.Column(db.Integer(), primary_key=True)
    id_project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    name = db.Column(db.String(), default='типовой документ')
    link = db.Column(db.String())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


class ProjectQuestions(db.Model):
    __tablename__ = 'project_questions'
    id = db.Column(db.Integer(), primary_key=True)
    id_project = db.Column(db.Integer(), db.ForeignKey('projects.id'))
    questions = db.Column(db.Text(), default='тупой вопрос')
    solution = db.Column(db.Text(), default='тупой ответ')
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


