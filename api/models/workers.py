# -*- coding: utf-8 -*-
from api import db
from datetime import datetime
from api.models.clients import MClients,MContacts,MClientPC,MBlockHistory


class MWorker(db.Model):
    __tablename__ = 'worker'
    id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    fio = db.Column(db.String(), nullable=False)
    work_phone = db.Column(db.String(), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    remove = db.Column(db.Boolean(), default=False)
    id_org_name = db.Column(db.Integer(), db.ForeignKey('org_name.id'))
    id_subversion = db.Column(db.Integer(), db.ForeignKey('subversion.id'))
    id_token = db.relationship('MToken', backref='workers_id', lazy='dynamic')
    id_workerconf = db.relationship('MWorkerConf', backref='workerconf_id', lazy='dynamic')
    id_call = db.relationship('MCall', backref='call_id', lazy='dynamic')

    def __repr__(self):
        return self.id


class MOrgName(db.Model):
    __tablename__ = 'org_name'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    code = db.Column(db.String(), unique=True)
    id_worker = db.relationship('MWorker', backref='orgname_id', lazy='dynamic')
    id_Clients = db.relationship('MClients', backref='orgname_id', lazy='dynamic')
    subversion_id = db.relationship('MSubdivision', backref='orgname_id', lazy='dynamic')

    def __repr__(self):
        return self.id


class MSubdivision(db.Model):
    __tablename__ = 'subversion'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    sub_cheff = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(), nullable=False)
    org_name = db.Column(db.Integer(), db.ForeignKey('org_name.id'))
    id_worker_subdivision = db.relationship('MWorker', backref='subversion_orgname', lazy='dynamic')
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow)
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id

class MToken(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer(), primary_key=True)
    token = db.Column(db.String, nullable=False)
    name = db.Column(db.String(), nullable=False)
    worker_id = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    sys_info = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    update_on = db.Column(db.DateTime(), default=datetime.utcnow)
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id

class MWorkerConf(db.Model):
    __tablename__ = 'worker_conf'
    id = db.Column(db.Integer(), primary_key=True)
    worker_id = db.Column(db.Integer(), db.ForeignKey('worker.id'))

    def __repr__(self):
        return self.id