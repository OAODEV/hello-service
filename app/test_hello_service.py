"""
Unit tests will be run inside the container, by the ops platform,
testing the code units in the contained environment.

The Dockerfile adds everything needed to run the tests into the
container in order to run the tests in the same environment that will
be deployed.

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
