import os

import SimpleHTTPServer
import SocketServer

def my_id():
    return os.getenv('HOSTNAME')

def make_index():
    with open("index.html", "w") as htmlfile:
        htmlfile.write("<h1>{}</h1>".format(my_id()))

if __name__ == "__main__":
    make_index()
    PORT = 8000
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()
