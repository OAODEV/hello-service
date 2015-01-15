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
        response = urllib2.urlopen("http://localhost:8001")
        self.assertEqual(response.code, 200)

        text = response.read()
        self.assertTrue("Hello" in text or "Hi" in text)

    def test_envars_are_set(self):
        """
        The default config included in this project should be set up to have
        envars that appear in the responce.

        This test assumes that these envars are `Environment_Name` and
        `template`.

        template should come from accept.conf

        """

        response = urllib2.urlopen("http://localhost:8001")
        first_line = response.readline()
        second_line = response.readline()
        self.assertTrue(re.search("Message from \w+.", first_line))
        self.assertTrue("<h3>Hi! I'm" in second_line)
        self.assertTrue("!!</h3>" in second_line)

    def test_can_pass(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
