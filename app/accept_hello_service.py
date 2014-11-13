import unittest
import urllib2
from multiprocessing import Process
from serve_hello import main

class AcceptHello(unittest.TestCase):

    def setUp(self):
        self.p = Process(target=main)
        self.p.start()

    def tearDown(self):
        self.p.terminate()


    def test_service_says_hello(self):
        response = urllib2.urlopen("http://localhost:8000")
        self.assertEqual(response.code, 200)

        text = response.read()
        self.assertTrue("Hello" in text or "Hi" in text)

    def test_can_pass(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
