import os
import SocketServer

def my_id():
    return os.getenv('HOSTNAME')

class HelloHandler(SocketServer.StreamRequestHandler):
    """
    say hello to requesters!

    """

    def handle(self):
        self.wfile.write("<h1>Hello from {}".format(my_id()))

if __name__ == "__main__":
    httpd = SocketServer.TCPServer(("", 8000), HelloHandler)
    httpd.serve_forever()
