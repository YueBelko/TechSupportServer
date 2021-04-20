# -*- coding: utf-8 -*-
from api import db
from datetime import datetime
from sqlalchemy.sql import func
from api.models.calls import MCall

class MClients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    unp = db.Column(db.String())
    phone = db.Column(db.String())
    u_address = db.Column(db.String())
    email = db.Column(db.String())
    block = db.Column(db.Boolean(), default=False)
    blocking_reason = db.Column(db.Text)
    remove = db.Column(db.Boolean(), default=False)
    support_time = db.Column(db.Integer(), default=0)
    orgname = db.Column(db.Integer(), db.ForeignKey('org_name.id'))
    id_contacts = db.relationship('MContacts', backref='id_contacts', lazy='dynamic')
    id_block_history = db.relationship('MContacts', backref='id_block_history', lazy='dynamic')
    id_client_pc = db.relationship('MClientPC', backref='id_client_pc', lazy='dynamic')
    id_client_call = db.relationship('MCall', backref='id_client_call', lazy='dynamic')


    def __repr__(self):
        return self.id


class MContacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer(), primary_key=True)
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    fio = db.Column(db.String())
    position = db.Column(db.String())
    phone = db.Column(db.String())
    email = db.Column(db.String())
    remove = db.Column(db.Boolean(),default=False)
    id_client_call = db.relationship('MCall', backref='id_contact_call', lazy='dynamic')


    def __repr__(self):
        return self.id


class MBlockHistory(db.Model):
    __tablename__ = 'block_history'
    id = db.Column(db.Integer(), primary_key=True)
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    data_block = db.Column(db.DateTime(), default=func.now())
    blocking_reason = db.Column(db.Text())
    status = db.Column(db.Boolean(), default=False)
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id


class MClientPC(db.Model):
    __tablename__ = 'clients_pc'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    id_clients = db.Column(db.Integer(), db.ForeignKey('clients.id'))
    rdesk_soft = db.Column(db.String())
    rdesk_id = db.Column(db.String())
    remove = db.Column(db.Boolean(), default=False)

    def __repr__(self):
        return self.id