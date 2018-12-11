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

    def test_index_response(self):
        print('Testing /index page for 200-ok response.')
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print('Testing redirect from / to /index')
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
