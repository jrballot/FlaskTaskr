#coding=utf-8

import os
import unittest
from project import app,db
from project._config import basedir
from project.models import User
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

    def test_user_can_register(self):
        new_user = User("michael","michael@mherman.org","michaelhermen")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == "michael"

    def login(self, name, password):
        return self.app.post('/',data=dict(
            name=name, password=password ), follow_redirects=True)

    def logout(self):
        return self.app.get('logout/',follow_redirects=True)


    def register(self, name, email, password, confirm):
        return self.app.post('register/',data=dict(name=name,email=email,password=password,confirm=confirm), follow_redirects=True)




    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sing in to access your task list', response.data)


    def test_user_cannot_login_unless_registered(self):
        response = self.login('foo','bar')
        self.assertIn(b'Invalid username or password.',response.data)


    def test_user_can_login(self):
        self.register('julioballot','admin@gmail.com','admin123','admin123')
        response = self.login('julioballot','admin123')
        self.assertIn(b'Welcome!', response.data)

    def test_invalid_form_data(self):
        self.register('julioballot','admin@gmail.com','admin123','admin123')
        response = self.login('alert("alert box!");','admin123')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.',response.data)

    def test_user_registration(self):
        self.app.get('register/',follow_redirects=True)
        response = self.register('julioballot','admin@gmail.com','admin123','admin123')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/',follow_redirects=True)
        self.register('julioballot','admin@gmail.com','admin123','admin123')
        self.app.get('register/',follow_redirects=True)
        response = self.register('julioballot','admin@gmail.com','admin123','admin123')
        self.assertIn(b'That username and/or email already exist.', response.data)


    def test_logged_in_users_can_logout(self):
        self.register('julioballot','admin@gmail.com','admin123','admin123')
        self.login('julioballot','admin123')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    # para esse teste foi necessario colocar login_required na função de logout dentro do controller(views.py)
    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)

    def test_logged_in_users_can_access_tasks_page(self):
        self.register('Fletcher','fletcher@realpython.com','python101','python101')
        self.login('Fletcher','python101')
        response = self.app.get('tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:',response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)





if __name__ == "__main__":
    unittest.main()
