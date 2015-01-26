"""
The service responds to requests with a greeting using the built in
python http modules.

"""
import os
import SocketServer

"""
The actual greeting is defined in a library that the hello service
depends on. hellolib is expected to be in the environment at this stage
and therefor is installed when docker builds the image. This is defined
in the Dockerfile.

"""

from hellolib import hello

class HelloHandler(SocketServer.StreamRequestHandler):
    """
    Say hello to requesters using the built in python http modules.

    """

    def handle(self):
        template = "<h1>{}</h1><h2>from: {}</h2>"
        self.wfile.write(template.format(hello(),
                                         os.environ['Environment_name']))

"""
When this file is run, a TCP server will listen on port 8001 and serve
the greeting to all requests.

The Dockerfile defines this as the service to run by default, therefor
when the container is run that container will be listening on port
8001 and serve the greeting to all requests.

"""

httpd = SocketServer.TCPServer(("", 8001), HelloHandler)

def main():
    httpd.serve_forever()

if __name__ == "__main__":
    main()
