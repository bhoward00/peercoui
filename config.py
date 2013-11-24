import os

_basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfiguration(object):
    DEBUG = False
    TESTING = False

    ADMINS = frozenset(['bhoward@lexmachina.com'])
    SECRET_KEY = 'SecretKeyForSessionSigning'

    THREADS_PER_PAGE = 8

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "somethingimpossibletoguess"

    #RECAPTCHA_USE_SSL = False
    #RECAPTCHA_PUBLIC_KEY = 'blahblahblahblahblahblahblahblahblah'
    #RECAPTCHA_PRIVATE_KEY = 'blahblahblahblahblahblahprivate'
    #RECAPTCHA_OPTIONS = {'theme': 'white'}

    #DATABASE = 'app.db'
    #DATABASE_PATH = os.path.join(_basedir, DATABASE)
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
    SQLALCHEMY_DATABASE_URI = 'postgresql://bhoward@localhost:5432/GPeerCoDB'

    
    #SERVERNAME='localhost:5001'


    DIRS_TO_MONITOR_FOR_RELOAD = ['app/templates',]
