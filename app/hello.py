import SocketServer

from hellolib import hello

class HelloHandler(SocketServer.StreamRequestHandler):
    """
    say hello to requesters!

    """

    def handle(self):
        self.wfile.write(hello())

httpd = SocketServer.TCPServer(("", 8000), HelloHandler)

if __name__ == "__main__":
    httpd.serve_forever()

