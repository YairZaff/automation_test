import http.server
import socketserver
import socket
socket.gethostbyname(socket.gethostname())

class test_server():
    def __init__(self):
        self.PORT = 8000
        self.Handler = http.server.SimpleHTTPRequestHandler
      
    def start(self):
        with socketserver.TCPServer(("", self.PORT), self.Handler) as httpd:
            print("serving at ", socket.gethostbyname(socket.gethostname())+":"+self.PORT)
            httpd.serve_forever()


if __name__ == "__main__":
    my_server=test_server()
    my_server.start()