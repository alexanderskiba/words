import unittest
import sys
sys.path.insert(0, '/Users/aleksandrskiba/Documents/python_kib_project/main')
from main import app


class TestApi(unittest.TestCase):
    # def test_registration_1(self):
    #     """ json correct  """
    #     passwd = {"password": 6666}
    #     with app.test_client() as client:
    #         result = client.post('/Server/registration/flexer2', headers=passwd)
    #         self.assertEqual(result.json, {'info': 'incorrect data',
    #                                        'status': True})

    def test_authentication_1(self):
        """ json correct  """
        passwd = {"password": 6666}
        with app.test_client() as client:
            result = client.post('/Server/authentication/flexer', headers=passwd)
            self.assertEqual(result.json, {'status': True, 'user_id': 2})

    def test_authentication_2(self):
        """ json not correct  """
        passwd = {"password": 'vkdjn33'}
        with app.test_client() as client:
            result = client.post('/Server/authentication/flexer', headers=passwd)
            self.assertEqual(result.json, {'info': 'this login already exists', 'status': False})
            self.assertEqual(result.status_code, 200)

    def test_authentication_3(self):
        """ json not correct  """
        passwd = {"passwordbsldksbdlv": '6666'}
        with app.test_client() as client:
            result = client.post('/Server/authentication/flexer', headers=passwd)
            self.assertEqual(result.json, {"status": False})

    def test_authentication_4(self):
        """ json not correct  """
        passwd = {"passwordbsldksbdlv": '6666'}
        with app.test_client() as client:
            result = client.post('/Server/authenticationiudbwle/flexer', headers=passwd)
            self.assertEqual(result.status_code, 404)

    def test_create_card_1(self):
        """ json correct  """
        data = {"underground": 'подземелье'}
        with app.test_client() as client:
            result = client.post('/Server/create_card/2', json=data)
            self.assertEqual(result.json, {"status": True})

    def test_update_card_1(self):
        """ json correct  """
        data = {'underground':['salam','салам']}
        with app.test_client() as client:
            result = client.post('/Server/update_card/2', json=data)
            self.assertEqual(result.json, {"status": True})


    def test_update_card_2(self):
        """  not existing card  """
        data = {'dfdfsdcsdf':['vladimir','putin']}
        with app.test_client() as client:
            result = client.post('/Server/update_card/2', json=data)
            self.assertEqual(result.json, {"status": False})


    def test_delete_card_(self):
        """  not existing card  """
        data = {'cat': ''}
        with app.test_client() as client:
            result = client.post('/Server/delete_card/2', json=data)
            self.assertEqual(result.json, {'delete card': 'cat', 'status': True}
)


















if __name__ == '__main__':
    unittest.main()
