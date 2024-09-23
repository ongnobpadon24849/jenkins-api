import unittest
from flask import Flask
from flask_api.app import app 

class FlaskTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "SDPX GROUP 3")

    def test_getcode(self):
        tester = app.test_client(self)
        response = tester.get('/getcode')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "SDPX GROUP 3 GET CODE 200 OK?")

    def test_plus_valid(self):
        tester = app.test_client(self)
        response = tester.get('/plus/3/4')
        self.assertEqual(response.status_code, 200)
        self.assertIn('INPUT 3 + 4 OUTPUT', response.data.decode('utf-8'))
        self.assertIn('plus', response.data.decode('utf-8'), 7)

    def test_plus_invalid(self):
        tester = app.test_client(self)
        response = tester.get('/plus/3/abc')
        self.assertEqual(response.status_code, 200)
        self.assertIn('error_msg', response.data.decode('utf-8'), 'Invalid input')

if __name__ == '__main__':
    unittest.main()
