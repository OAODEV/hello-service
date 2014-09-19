import SocketServer

from hellolib import hello

class HelloHandler(SocketServer.StreamRequestHandler):
    """
    say hello to requesters!

    This is the a mimal toy example of a service.
    It simply responds with the result of an imported hello function.

    """

    def handle(self):
        self.wfile.write(hello())

httpd = SocketServer.TCPServer(("", 8000), HelloHandler)

if __name__ == "__main__":
    httpd.serve_forever()

