import unittest
from web import app


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tester = app.test_client(cls)

    def test_index(self):
        response = self.tester.get('/')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_capture(self):
        response = self.tester.get('/capture')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_upload(self):
        response = self.tester.get('/upload')
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_cloning(self):
        response = self.tester.get('/cloning')
        status_code = response.status_code
        self.assertEqual(status_code, 302)   # redirect

    def test_process(self):
        response = self.tester.get('/process')
        status_code = response.status_code
        self.assertEqual(status_code, 302)   # redirect


if __name__ == '__main__':
    unittest.main()
