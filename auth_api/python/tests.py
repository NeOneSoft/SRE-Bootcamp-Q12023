import os
import requests
import unittest
from methods import Token, Restricted


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.admin_token = os.environ.get('ADMIN_TOKEN')
        self.admin_password = os.environ.get('ADMIN_PASSWORD')
        self.convert = Token()
        self.validate = Restricted()

    def test_generate_token(self):
        self.assertEqual(self.admin_token, self.convert.generate_token('admin', self.admin_password))

    def test_access_data(self):
        token = "Bearer " + self.admin_token
        result = self.validate.access_data(token)
        self.assertEqual(result, 'You are under protected data')


class TestAPI(unittest.TestCase):

    def test_url_root(self):
        res = requests.get("http://127.0.0.1:8000/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, "OK")

    def test_url_health(self):
        res = requests.get("http://127.0.0.1:8000/_health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, "OK")

    def test_url_login_no_data(self):
        res = requests.post("http://127.0.0.1:8000/login")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "username and password is required")

    def test_url_login_invalid_credentials(self):
        res = requests.post("http://127.0.0.1:8000/login", data={'username': 'admin', 'password': 'wrong_password'})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res.json()["error"], "Unauthorized")

    def test_url_protected_no_token(self):
        res = requests.get("http://127.0.0.1:8000/protected")
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "Authorization header is required")

    def test_url_protected_invalid_token(self):
        headers = {
            "Authorization": "invalid_token"
        }
        res = requests.get("http://127.0.0.1:8000/protected", headers=headers)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json()["error"], "Invalid token")


if __name__ == '__main__':
    unittest.main()
