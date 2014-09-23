"""
Acceptance tests will be run outside the container, by fabric, testing the
behavior of the contained service.

"""

import os

# with the service running locally on the above port and address,
# we can start to assert our expectations
import unittest
from urllib2 import urlopen

class HelloServiceAcceptanceTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_says_hello(self):
        # fabric will start our service in the local environment.
        # it will be found at http://localhost:8000
        response = urlopen("http://localhost:8000").read()

        # the response should be a greeting
        self.assertTrue("Hasdfi" in response or "Hello" in response)

        # the response should say who it is
        self.assertTrue("I'm" in response or "my name is" in response)


    def test_can_pass(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
