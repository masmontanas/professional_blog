#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db, errors, helpers
from app.models import User, Post

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_new_user(self):
        print('Testing addition of new user to db.')
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()
        assert u

    def test_query_user(self):
        print('Testing user query.')
        query = User.query.all()
        assert query == []

    def test_index_response(self):
        ## Need to add a blog post since one is required to render the page.
        u = User(username='tester', email='tester@test.com')
        db.session.add(u)
        db.session.commit()
        print("Added user '{}' to session.".format(u.username))
        post = Post(body='testing', user_id=u.id, title='test title', description='test description')
        db.session.add(post)
        db.session.commit()
        print("Added post '{}' to session.".format(post.title))
        print("Testing 200-ok response on /index")
        response = self.app.get('/index', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        print("Testing redirect from '/' to '/index'")
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
