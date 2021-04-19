# -*- coding: utf-8 -*-
from api import db
from api.models.workers import MWorker, MWorkerConf, MToken, MSubdivision, MOrgName
import datetime

def normal(string):
    string = string.lower()
    return string

def its_admin(token):
    tok = MToken.query.filter_by(token=token).first()
    if hasattr(tok,'id'):
        str(tok.workers_id.admin)
        return str(tok.workers_id.admin)
    else:
        return False

def get_orgname(token):
    tok = MToken.query.filter_by(token=token).first()
    if hasattr(tok, 'id'):
        return tok.workers_id.orgname_id
    else:
        return 1
