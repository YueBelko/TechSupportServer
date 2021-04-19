# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import Flask, request
from api import db


class Ind(Resource):
    def get(self):
        return {'Request': 'Get', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201

    def post(self):
        print('token : ' + request.form['token'])
        print('values : ' + request.form['values'])
        return {'Request': 'Post', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201

    def delete(self):
        return {'Request': 'Delete', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201

    def options(self):
        return {'Request': 'OPTIONS', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201

    def patch(self):
        return {'Request': 'PATCH', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201

    def put(self):
        return {'Request': 'Put', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201

    def delete(self):
        return {'Request': 'Delete', 'API Version': 'V 0.001', 'Front': 'Jopka', 'Server': 'TrueCoolServer'}, 201