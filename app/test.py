import os
import unittest
import urllib2
from multiprocessing import Process

from hello import my_id, httpd

class DockerHelloTests(unittest.TestCase):

    def setUp(self):
        os.environ['HOSTNAME'] = "test-hostname"
        self.server = Process(target=httpd.serve_forever)
        self.server.start()

    def tearDown(self):
        self.server.terminate()

    def test_my_id(self):
        self.assertTrue(len(my_id()) > 5)
        self.assertEqual(my_id(), my_id())
        self.assertEqual(type(my_id()), str)

    def test_hello_handler(self):
        self.assertEqual(
            urllib2.urlopen("http://localhost:8000").read().strip(),
            '<h1>Hello from test-hostname</h1>')

    def test_can_pass(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
