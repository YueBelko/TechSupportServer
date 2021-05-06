# -*- coding: utf-8 -*-
from api import app
# from flask_sqlalchemy import SQLAlchemy


if __name__ == '__main__':

    # import os
    # HOST = os.environ.get('SERVER_HOST', 'localhost')
    # try:
    # PORT = int(os.environ.get('SERVER_PORT', '55555'))
    # except ValueError:
    # PORT = 55555
    # app.run(HOST, PORT)
    app.run(host='0.0.0.0', port=5000)
