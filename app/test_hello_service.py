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
        pass

    def tearDown(self):
        pass

    def test_envars_are_set(self):
        """
        ensure that the envars expected to be present have been injected by
        the platform when testing (in the same way they will when deployed)

        This test only verifies that `fab test` sets the envars

        """

        self.assertTrue("Environment_name" in os.environ)
        self.assertEqual("<h1>Hi! I'm {hostname} in {env_name}!!</h1>",
                         os.environ['template'])

    def test_hello_handler(self):
        # set up
        mock_wfile = Mock()
        handler = HelloHandler(Mock(), Mock(), Mock())
        handler.wfile = mock_wfile

        # run SUT
        handler.handle()

        # confirm
        self.assertEqual(mock_wfile.write.call_count, 1)

    def test_can_pass(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
