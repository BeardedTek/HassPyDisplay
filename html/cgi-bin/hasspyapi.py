#!/usr/bin/python
#   HassPyAPI - Python 3 Class for accessing the Home Assistant REST API
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

class hasspyapi:
    def __init__(self,config):
        # Requires config[host,token,domain,service,entity,logfile]
        self.debug_output = []
        self.forward = ""
        self.host = config[0]
        self.token = config[1]
        self.domain = config[2]
        self.service = config[3]
        self.entity = config[4]
        self.logfile = config[5]
        self.debug = config[6]
        self.attrval = ""
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
        if self.debug == True:
            self.write_log(['verbose',"post/url",self.url])
            self.write_log(['verbose',"post/headers",self.headers])
            self.write_log(['verbose',"post/data",self.data])
            
        response = requests.post(self.url,headers=self.headers,data=self.data)
        return response.text
    
    def get(self):
        import requests
        import json
        if self.debug == True:
            self.write_log(['verbose',"get/url",self.url])
            self.write_log(['verbose',"get/headers",json.dumps(self.headers)])
        response = requests.get(self.url,headers=self.headers)
        return response.text

    def get_status(self):
        import json
        self.attributes = []
        self.other = []
        self.context = []
        input = self.get()
        if self.debug == True:
            self.write_log(['verbose',"get_status/json",input])
        status = json.loads(input)
        for key in status:
            if key == 'entity_id':
                self.entity_id = status[key]
            elif key == 'state':
                self.state = status[key]
            elif key == 'last_changed':
                self.last_changed = status[key]
            elif key == 'last_updated':
                self.last_updated = status[key]
            elif key == 'context':
                attributes = status[key]
                for attribute in attributes:
                    self.context.append([attribute,attributes[attribute]])
            elif key == 'attributes':
                attributes = status[key]
                for attribute in attributes:
                    self.attributes.append([attribute,attributes[attribute]])
            else:
                self.other.append([key,status[key]])
        self.status = [self.entity_id,self.state,self.last_changed,self.last_updated,self.attributes,self.context,self.other]
        #self.status structure
        #[0] = entity_id
        #[1] = state
        #[2] = last_changed
        #[3] = last_updated
        #[4] = attributes
        #[5] = context
        #[6] = anything not captured by the above categories In most cases it won't capture anything.
        return self.status

    def execute(self):
        import json
        if self.service == 'status':
            output = self.get_status()
            if self.debug == 'verbose':
                self.write_log(['verbose',"execute/status/json",json.dumps(self.get())])
                self.write_log(['verbose',"execute/status/output",output])
            return output
        elif self.service != 'status':
            if self.debug == 'verbose':
                self.write_log(['verbose',"execute/other/json",self.post()])
            return self.post()

    def write_log(self,output):
        logfile = open(self.logfile, "a")
        from datetime import datetime
        line = "[ "+ datetime.now().strftime("%Y-%m-%d @ %H:%M:%S") +" ] " + output[0] + " >> " + output[1] + " | " + output[2] + "\n"
        logfile.write(line)