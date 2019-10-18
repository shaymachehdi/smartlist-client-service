import json
import unittest


from flask import request, Flask, current_app
from flask_login import login_user
from sqlalchemy.sql.functions import user

from userservice import app
# set our application to testing mode
from userservice.myservices.users.routes import users
from userservice.myservices.users.models import Registreduser

app.register_blueprint(users)

app.testing = True
app_context = app.app_context()


# app_context.push()

class TestApi(unittest.TestCase):

    # create  acocunt
    def test_create_account(self):
        data = dict(email='test@gmail.com', password='0000000', firstname='shayma',
                    lastname='chehdi',
                    phone_number='51999517', dateOfBirth=None, adresse='tunis')
        with  app.app_context():
            self.client = app.test_client()
            response = self.client.post('/user/signup', data=json.dumps(data), content_type='application/json')
            assert response.status_code == 200

    # delete user
    def test_delete_user(self):
        data = dict(email='test@gmail.com', id=1, enabled=True)
        with  app.app_context():
            self.client = app.test_client()
            response = self.client.post('/user/delete/<int:id>/<string:email>', data=json.dumps(data),
                                        content_type='application/json')





    # login
    def test_login(self):
        data = dict(email='test@gmail.com', password='0000000')
        with  app.app_context():
            self.client = app.test_client()
            response = self.client.post('/user/login', data=json.dumps(data), content_type='application_json')



    # add group
    def test_add_group(self):
        data = dict(title='test', date_created='2010-04-02', created_by='1',
                    fllowers='chehdi')
        with  app.app_context():
            # resp = client.get('/group')

            self.client = app.test_client()
            response = self.client.post('/group', data=json.dumps(data), content_type='application/json')

    # delete group
    def test_delete_group(self):
        data = dict(id=1, enabled=True)
        with  app.app_context():
            self.client = app.test_client()
            response = self.client.post('/group/delete/<int:id>', data=json.dumps(data),
                                        content_type='application/json')

    # add follower

    def test_add_follower(self):
        data = dict(group_follower_id='1', follower_id='2', followed_at='2010-04-02',
                    )
        with  app.app_context():
            self.client = app.test_client()
        response = self.client.post('/follow', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    # delete follower
    def test_delete_follower(self):
        data = dict(id=1, enabled=True)
        with  app.app_context():
            # resp = client.get('/follow')

            self.client = app.test_client()
            response = self.client.post('/follow/delete/<int:id>', data=json.dumps(data),

                                        content_type='application/json')

    # add device
    def test_add_device(self):
        data = dict(localisation='36.7366693,10.2965886', code_device='2225', email='test@gmail.com', install_at='2019-07-01',
                    user_id='5', code='55', levelConfidence_device='5'
                    )
        with  app.app_context():
            # resp = client.get('/follow')

            self.client = app.test_client()
        response = self.client.post('/follow', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200

    # delete device
    def test_delete_device(self):
        data = dict(id=1, enabled=True)
        with  app.app_context():
            # resp = client.get('/device')

            self.client = app.test_client()
        response = self.client.post('/device/delete/<int:id>', data=json.dumps(data),
                                    content_type='application/json')


if __name__ == "__main__":
    unittest.main()
