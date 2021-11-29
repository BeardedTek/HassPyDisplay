#   HassPyAPI - Python 3 CGI Script for accessing the Home Assistant REST API
#   Copyright (C) 2021  The Bearded Tek (http://www.beardedtek.com) William Kenny
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#!/usr/bin/python
import cgi
class hasspyapi:
    def __init__(self):
        self.cgidata = cgi.FieldStorage()
        self.debug = self.cgidata.getvalue('debug')
        self.forward = self.cgidata.getvalue('forward')
        self.silent = self.cgidata.getvalue('silent')
        if self.forward == None:
            self.forward = 'hasspyapi.cgi'
        if self.forward == 'false' and self.debug != 'true':
            print("content-type: text/html\n\n<html><body>")
        elif self.forward != 'false' and self.debug == "true":
            print("content-type: text/html\n\n<html><body>")
            print(f"<a href='{self.forward}'>Continue to {self.forward}</a>")
        elif self.forward != 'false' and self.silent == 'false':
            print('content-type: text/plain\n\n')
        else:
            print(f"Status: 303 See other\nLocation: {self.forward}\n\n")
        if self.debug == 'true':
            print(f"CGI DATA:<br><br>{self.cgidata}<br><br><br>")
        self.host = self.cgidata.getvalue('host')
        self.method = self.cgidata.getvalue('method')
        self.domain = self.cgidata.getvalue('domain')
        self.service = self.cgidata.getvalue('service')
        self.entity = self.cgidata.getvalue('entity')
        self.token = self.cgidata.getvalue('token')
        self.attr = self.cgidata.getvalue('attr')
        self.attrval = self.cgidata.getvalue('attrval')
        self.headers = {
        'Authorization': 'Bearer '+self.token,
        'content-type': 'application/json',
        }
        if self.service == 'status':
            #/api/states/<entity_id>
            self.url = self.host+"/api/states/"+self.entity
        elif self.service == 'set':
            self.url = self.host+"/api/states/"+self.entity
            self.data = '{"state":"'+self.attrval+'"}'
        else:
            #/api/services/<domain>/<service>
            self.url = self.host+"/api/services/"+self.domain+"/"+self.service
            self.data = '{"entity_id": "'+self.entity+'"}'
    def post(self):
        import requests
        if self.debug == "true":
            print("Data Sent to HA<br><br>")
            print(self.url+"<br><br>")
            print(self.headers)
            print("<br><br>")
            print(self.data)
            print("<br><br>")
            
        response = requests.post(self.url,headers=self.headers,data=self.data)
        return response.text
    
    def get(self):
        import requests
        if self.debug == "true":
            print("content-type: text/html\n\n<html><body>")
            print(self.url+"<br><br>")
            print(self.headers)
            print("<br><br>")
        response = requests.get(self.url,headers=self.headers)
        return response.text
    def execute(self):
        import json
        if self.service == 'status' and self.debug == 'true':
            print(json.dumps(self.get()).replace(",",",\n").replace("{","{\n"))
        elif self.service == 'status' and self.silent == 'false':
            print(json.dumps(self.get()).replace(",",",\n").replace("{","{\n").replace("\\\"","'"))
        elif self.service == 'status' and self.debug != 'true':
            self.get()
        elif self.service != 'status' and self.debug == 'true':
            print(self.post())
        elif self.service != 'status' and self.debug != 'true':
            self.post()
    def debug_output(self):
        print("content-type: text/plain\n\n")
        print(self.cgidata)
        print("\n\n\n\n\n\n\n\n\n\n\n")
        print(f"URL:\n{self.url}\n\n\n")
        print(f"host: {self.host}\n\n\n method: {self.method}\n\n\n domain: {self.domain}\n\n\n")
        print(f"service: {self.service}\n\n\n entity: {self.entity}\n\n\n debug: {self.debug}\n\n\n")
def main():
    haapi = hasspyapi()
    haapi.execute()

main()
