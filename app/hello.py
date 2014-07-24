import os
import SocketServer

def my_id():
    return os.getenv('HOSTNAME')

class HelloHandler(SocketServer.StreamRequestHandler):
    """
    say hello to requesters!

    """

    def handle(self):
        self.wfile.write("<h1>Hello from {}</h1>".format(my_id()))

httpd = SocketServer.TCPServer(("", 8000), HelloHandler)

if __name__ == "__main__":
    httpd.serve_forever()

