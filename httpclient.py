#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, James Schaefer-Pham, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse as parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def parse_url(url):
        pass

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def get_code(self, data):
        try:
            head = data.split("\r\n")[0]
            code = head.split()[1]
            return int(code)
        except:
            return 404

    def get_headers(self,data):
        headers = data.split("\r\n\r\r")[0]
        return headers.split()[1:]

    def get_body(self, data):
        try:
            content = data.split("\r\n\r\n")[1]
        except:
            return ""
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""

        scheme, netloc, path, query, fragment = parse.urlsplit(url)
        split_netloc = netloc.split(":")

        if not "/" in path:
            path = "/"
        
        if len(split_netloc) == 2:
            self.connect(split_netloc[0], int(split_netloc[1]))
        else:
            self.connect(split_netloc[0], 80)

        # Send request
        request = f"GET {path} HTTP/1.1\r\nHost: {split_netloc[0]}\r\nConnection: close\r\n\r\n"
        self.sendall(request)
        #self.socket.shutdown()

        # Recieve and process
        response = self.recvall(self.socket)
        code = self.get_code(response)
        body = self.get_body(response)
        headers = self.get_headers(response)

        print(f"Code: {code}\nHeaders: {headers}\nBody: {body}")

        self.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""

        if args:
            content = parse.urlencode(args)
            content_len = len(args)
        else:
            content = ""
            content_len = 0

        scheme, netloc, path, query, fragment = parse.urlsplit(url)
        split_netloc = netloc.split(":")

        if not "/" in path:
            path = "/"
        
        if len(split_netloc) == 2:
            self.connect(split_netloc[0], int(split_netloc[1]))
        else:
            self.connect(split_netloc[0], 80)

        # Send request
        request = f"GET {path} HTTP/1.1\r\nHost: {split_netloc[0]}\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: {content_len}\r\nConnection: close\r\n\r\n{content}"
        self.sendall(request)
        #self.socket.shutdown()

        # Recieve and process
        response = self.recvall(self.socket)
        code = self.get_code(response)
        body = self.get_body(response)
        headers = self.get_headers(response)

        print(f"Code: {code}\nHeaders: {headers}\nBody: {body}")

        self.close()

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"


    # TODO HANDLE ARGS (probably for POSt)


    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
