import os

def configureApp(app):
    END_POINT = os.environ['END_POINT']
    USER_NAME = os.environ['USER_NAME']
    PASSWORD = os.environ['PASSWORD']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+ USER_NAME + ':' + PASSWORD + '@' + END_POINT
