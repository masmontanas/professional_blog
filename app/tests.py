#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db, errors, helpers
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_new_user(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        assert u

    def test_query_user(self):
        query = User.query.all()
        assert query == []


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
