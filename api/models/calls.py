# -*- coding: utf-8 -*-
from api import db
from datetime import datetime
from sqlalchemy.sql import func


class MCall(db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer(), primary_key=True)
    id_clients = db.Column(db.Integer())
    id_worker = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    time_in = db.Column(db.DateTime(), default=func.now())
    time_out = db.Column(db.DateTime(), default=func.now())
    reason_calls = db.Column(db.Text())
    id_project = db.Column(db.Integer())
    id_clients_contact = db.Column(db.Integer())
    call_ended = db.Column(db.Boolean(), default=False)
    remove = db.Column(db.Boolean(), default=False)
    def __repr__(self):
        return self.id


class MRequestTime(db.Model):
    __tablename__ = 'requesttime'
    id = db.Column(db.Integer(), primary_key=True)
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    id_worker = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    id_project = db.Column(db.Integer())
    id_request = db.Column(db.Integer())
    lead_time = db.Column(db.Integer())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id

class MOtherRequestTime(db.Model):
    __tablename__ = 'otherrequesttime'
    id = db.Column(db.Integer(), primary_key=True)
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    id_worker = db.Column(db.Integer(), db.ForeignKey('worker.id'))
    id_project = db.Column(db.Integer())
    completed_work = db.Column(db.Integer())
    lead_time = db.Column(db.Integer())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id