import unittest
from app import app


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    # def test_login(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/login', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
