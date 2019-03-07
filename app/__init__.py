from flask import Flask, url_for, redirect, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler 
from flask_moment import Moment
from flask_mail import Mail
from flask_minify import minify
#from mailchimp3 import MailChimp
from elasticsearch import Elasticsearch
from elasticapm.contrib.flask import ElasticAPM
import elasticapm
from flask_caching import Cache
import os
from flask_featureflags import FeatureFlag
import flask_featureflags as feature


app = Flask(__name__)
app.config.from_object(Config)

feature_flags = FeatureFlag(app)
    
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)
mail = Mail(app)
minify = minify(app=app)
#client = MailChimp(mc_api=app.config['MAILCHIMP_API_KEY'], mc_user=app.config['MAILCHIMP_USER_NAME'])
cache = Cache(app, config={'CACHE_TYPE': 'simple'})



if feature.is_active('search_feature'):   
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
else:
    app.elasticsearch = None

if feature.is_active('apm_feature'):
    app.config['ELASTIC_APM'] = {'SERVICE_NAME': 'testapmservice'}
    apm = ElasticAPM(app, logging=True)
else:
    apm = None


from app import routes, models, errors, helpers

bootstrap = Bootstrap(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='professional_blog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/professional_blog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter( '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('professional_blog startup')