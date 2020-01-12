import http.server
import socketserver
import socket
import os

class test_server():
    def __init__(self):
        self.PORT = 8000
        self.Handler = http.server.SimpleHTTPRequestHandler
        self.start_server(self.PORT,self.Handler)

    def start_server(self, port, handler):
        self.generate_index_file()
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("serving at ", socket.gethostbyname(socket.gethostname())+":"+str(port))
            httpd.serve_forever()
        

    def get_list_of_files(self,dir_name):
        list_of_files = os.listdir(dir_name)
        all_files = list()
        for entry in list_of_files:
            full_path = os.path.join(dir_name, entry)
            if os.path.isdir(full_path):
                all_files = all_files + self.get_list_of_files(full_path)
            else:
                all_files.append(full_path)
        return all_files

    def generate_index_file(self):
        content="<html>\n<head>\n\t<title>index</title>\n</head>\n<body>\n\t<h1>index</h1>\n\t<hr>\n"
        if os.path.exists("index.html"):
            os.remove("index.html")
        f=open("index.html","w")
        file_list=self.get_list_of_files(".")
        for file_path in file_list:
            content+="\t<a href = \""+file_path+"\">"+file_path+"</a><br>\n"
        content +="</body>\n</html>"
        f.write(content)
        f.close()
        
if __name__ == "__main__":
    my_server=test_server()

    