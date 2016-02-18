#coding=utf-8

import os
import unittest
from views import app,db
from _config import basedir
from models import User
TEST_DB='test.db'

# String de comparação devem ser exatamente iguais as que serão apresentadas na interface
# Endpoints também deve ter o caminho igual ao utilizados nas views

class AllTests(unittest.TestCase):

    # setup and teardown
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, name, password):
        return self.app.post('/',data=dict(
            name=name, password=password ), follow_redirects=True)
    def logout(self):
        return self.app.get('logout/',follow_redirects=True)

    def create_user(self,name,email,password):
        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()


    def create_task(self):
        return self.app.post('add/', data=dict(
            name="Go to the bank",
            due_date='02/05/2014',
            priority='1',
            posted_date='02/04/2014',
            status='1'
        ), follow_redirects=True)

    def create_user_and_login_and_get_tasks(self):
        self.create_user('Michael','michael@realpython.com','python')
        self.login('Michael','python')
        self.app.get('tasks/',follow_redirects=True)


    def create_admin_user(self):
        new_user = User(
            name="Superman",
            email="admin@realpython.com",
            password="allpowerfull",
            role="admin"
        )
        db.session.add(new_user)
        db.session.commit()

    def test_users_can_add_tasks(self):
        self.create_user_and_login_and_get_tasks()
        response = self.create_task()
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

    # teste de incersão de valor com erro
    def test_users_cannot_add_tasks_when_error(self):
        self.create_user_and_login_and_get_tasks()
        response = self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='02/04/2014',
            status='1'
        ), follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_users_can_complete_tasks(self):
        self.create_user_and_login_and_get_tasks()
        self.create_task()
        response = self.app.get("complete/1", follow_redirects=True)
        self.assertIn(b'The task is complete. Nice.', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user_and_login_and_get_tasks()
        self.create_task()
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user_and_login_and_get_tasks()
        self.create_task()
        self.logout()
        self.create_user('Fletcher','fletcher@realpython.com','python')
        self.login('Fletcher','python')
        self.app.get('tasks/',follow_redirects=True)
        response = self.app.get("complete/1", follow_redirects=True)
        self.assertNotIn(b'The task is complete. Nice.', response.data)
        self.assertIn(b'You can only update tasks that belong to you.', response.data)

    def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
        self.create_user_and_login_and_get_tasks()
        self.create_task()
        self.logout()
        self.create_user('Fletcher','fletcher@realpython.com','python')
        self.login('Fletcher','python')
        self.app.get('tasks/',follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertIn(b'You can only delete tasks that belong to you.', response.data)

    def test_default_user_role(self):
        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )
        db.session.commit()
        users = db.session.query(User).all()
        print users
        for user in users:
            self.assertEquals(user.role, 'user')

    def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
        self.create_user_and_login_and_get_tasks()
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login('Superman','allpowerfull')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1", follow_redirects=True)
        self.assertNotIn(
            "You can only update tasks that belong to you.",
            response.data
        )

    def test_admin_users_can_delete_tasks_that_are_not_created_by_them(self):
        self.create_user_and_login_and_get_tasks()
        self.create_task()
        self.logout()
        self.create_admin_user()
        self.login("Superman","allpowerfull")
        self.app.get("tasks/", follow_redirects=True)
        response = self.app.get("delete/1/", follow_redirects=True)
        self.assertNotIn(
            "You can only delete tasks that belong to you.",
            response.data
        )

if __name__ == "__main__":
    unittest.main()
