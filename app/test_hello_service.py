"""
Unit tests will be run inside the container, by fabric, testing the code units
in the contained environment.

This means that code for compiled systems should be added to the container to
allow the tests to be run in the contained environment. This creates consistancy
between the environment we run and the environment we build and test.

"""

import os
import unittest
from mock import MagicMock as Mock

from serve_hello import HelloHandler

class DockerHelloTests(unittest.TestCase):

    def setUp(self):
        self.old_hostname = None
        if 'HOSTNAME' in os.environ:
            self.old_hostname = os.environ['HOSTNAME']
        os.environ['HOSTNAME'] = "testhost"

    def tearDown(self):
        if self.old_hostname:
            os.environ['HOSTNAME'] = self.old_hostname

    def test_hello_handler(self):
        # set up
        mock_wfile = Mock()
        handler = HelloHandler(Mock(), Mock(), Mock())
        handler.wfile = mock_wfile

        # run SUT
        handler.handle()

        # confirm
        mock_wfile.write.assert_called_once_with("<h1>Hi! I'm testhost!</h1>")

    def test_can_pass(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
