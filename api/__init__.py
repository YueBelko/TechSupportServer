# -*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://caller:30197669@172.16.254.56/techsupport'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
app.config['FLASK_APP'] = 'run.py'
app.config['FLASK_DEBUG'] = 1


api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.resources.index import Ind
from api.resources.workers import ROrgName
from api.resources.RRes.rsubversion import RSubversion
from api.resources.RRes.rworkers import RWorkers
from api.resources.RRes.rtoken import RToken
from api.resources.RRes.rclients import RClients
from api.resources.RRes.rcontact import RContact
from api.resources.RRes.rclientpc import RClientpc
from api.resources.RRes.rblock import RBlock
from api.models.workers import MWorker, MOrgName, MSubdivision, MToken, MWorkerConf
from api.models.clients import MClients, MContacts, MBlockHistory, MClientPC
from api.models.calls import MCall,MRequestTime, MOtherRequestTime
from api.resources.RRes.rcalls import RCall
from api.models.projects import MProject, MProjectInfo, MProjectRequest, MRequestStatus, MChangeInTheProject
from api.resources.RRes.rproject import RProject

api.add_resource(Ind, '/')
api.add_resource(RWorkers, '/workers')
api.add_resource(ROrgName, '/orgname')
api.add_resource(RSubversion, '/subversion')
api.add_resource(RToken, '/token')
api.add_resource(RClients, '/clients')
api.add_resource(RContact, '/contacts')
api.add_resource(RClientpc, '/clientpc')
api.add_resource(RBlock, '/block')
api.add_resource(RCall, '/calls')
api.add_resource(RProject, '/project')





