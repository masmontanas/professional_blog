import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENVIRONMENT = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_POOL_RECYCLE = os.environ.get('SQLALCHEMY_POOL_RECYCLE') or 30
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or 1
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['sre_team_email@jouharyanconsulting.opsgenie.net']
    POSTS_PER_PAGE = os.environ.get('POSTS_PER_PAGE') or 5
    COMMENTS_PER_PAGE = os.environ.get('COMMENTS_PER_PAGE') or 5
    MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
    MAILCHIMP_USER_NAME = os.environ.get('MAILCHIMP_USER_NAME')
    MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
    MAILCHIMP_COMMENTOR_LIST_ID = os.environ.get('MAILCHIMP_COMMENTOR_LIST_ID')
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ELASTIC_APM = {}
    FEATURE_FLAGS = {
        'search_feature':False,
        'apm_feature': False
    }