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
        # set up expected/dependant envars
        os.environ['greeting'] = "test message"
        os.environ['HOSTNAME'] = "test"

    def tearDown(self):
        del os.environ['greeting']

    def test_hello_handler(self):
        # set up
        mock_wfile = Mock()
        handler = HelloHandler(Mock(), Mock(), Mock())
        handler.wfile = mock_wfile

        # run SUT
        handler.handle()

        # confirm
        self.assertEqual(mock_wfile.write.call_count, 1)
        expected_string = "<h1>test message</h1><h2>from: test</h2>"
        mock_wfile.write.assert_called_once_with(expected_string)

    def test_can_pass(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
