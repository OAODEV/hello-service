import os
import unittest

from hello import my_id, make_index

class DockerHelloTests(unittest.TestCase):

    def setUp(self):
        make_index()

    def tearDown(self):
        os.remove("index.html")

    def test_my_id(self):
        self.assertTrue(len(my_id()) > 5)
        self.assertEqual(my_id(), my_id())
        self.assertEqual(type(my_id()), str)

    def test_index(self):
        with open("index.html", "r") as htmlfile:
            self.assertTrue(my_id() == htmlfile.read())

    def test_can_pass(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
