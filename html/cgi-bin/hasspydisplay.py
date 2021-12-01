#!/usr/bin/python
#   HassPyDisplay - Python 3 CGI Script for Display of information from Home Assistant
#                   via a web interface
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


import cgi
import json
import string
class hasspydisplay:
    def __init__(self):
        self.token = ""
        self.host = ""
        self.css = ""
        self.debug = ""
        self.debugme = ""
        self.debug_output = []
        self.forward = ""
        self.js = ""
        self.input = ""
        self.page = ""
        self.page_title = ""
        self.page_json = ""
        self.data = ""
        self.items = []
        self.input = cgi.FieldStorage()
        self.test = self.input.getvalue('test')
        if self.input.getvalue('debugme') == 'true':
            self.debugme = True
        else:
            self.debugme = False
        if self.input.getvalue('debug') == 'true':
            self.debug = True
        else:
            self.debug = False
        if self.input.getvalue('page') != None:
            self.page_title = self.input.getvalue('page')
            self.page = "/var/www/html/json/"+self.page_title+".json"
        else:
            self.page = "/var/www/html/json/default.json"
        #self.debug_append("Page: "+self.page)

    def debug_append(self,output):
        self.debug_output.append(output)
    
    def print_debug(self):
        print("<div class='debug'>\n")
        num = 1
        for x in self.debug_output:
            print(f"<div class='debug_item'><span></span><span>{x}</span></div>\n")
            num += 1
        print("</div>\n")

    def get_config_list(self):
        import glob
        config_list = glob.glob('../json/*.json')
        for i in range(len(config_list)):
            config_list[i] = config_list[i].replace("../json/","").replace(".json","").replace("_"," ")
        return config_list

    def get_config(self):
        with open(self.page) as self.page_json:
            self.data = json.load(self.page_json)
            for key in self.data:
                if key == "config":
                    config = self.data[key]
                    #self.debug_append(json.dumps(self.data).replace("}","}<br>"))
                    self.token = config['token']
                    self.debug_append(self.token)
                    self.host = config['host']
                    self.debug_append(self.host)
                    self.forward = config['forward']
                    self.debug_append(self.forward)
                    self.image = config['image']
                    self.debug_append(self.image)
                    self.logfile = config['logfile']
                    self.debug_append(self.logfile)
                    css = config['css']
                    if css != None:
                        css_file = open(css)
                        self.css = css_file.read()
                    else:
                        self.css = "\n"
                    js = config['js']
                    if js != None:
                        js_file = open(js)
                        self.js = js_file.read()
                    else:
                        self.js = "\n"

    def get_items(self):
        i = 0
        with open(self.page) as self.page_json:
            self.data = json.load(self.page_json)
            for key in self.data:
                if key != "config":
                    entity = self.data[key]
                    entity_id = entity['entity']
                    action = entity['action']
                    domain = entity['domain']
                    label = key
                    onclick = "document.getElementById(\""+entity_id+"\").submit()"
                    
                    if self.items != None:
                        self.items.append([entity_id,label,onclick,action,domain])
                    else:
                        self.items = [entity_id,label,onclick,action,domain]
                i += 1
        self.debug_append(self.items)
    def print_header(self):
        print(f"content-type: text/html\n\n<html>\n<head>\n")
        print(f"<title>Home - {self.page_title.replace('_',' ')}</title>\n")
        print(f"<meta name='viewport' content='width=1000, initial-scale=1'>")
        self.print_css()
        self.print_js()
        print(f"</head>\n<body>\n<div class='container'>\n")

    def print_menu(self):
        menu_item = self.get_config_list()
        print(f"<div class='menu'>")
        for i in range(len(menu_item)):
            if i == 0:
                form = "<form id='default-menu' action=''>"
                form += "<input type='hidden' id='page' name='page' value='default'>"
                form += "Home"
                form += "</form>"
                print(f"<div class='menu_item default' onclick='document.getElementById(\"default-menu\").submit()'>{form}</div>")
            if menu_item[i] != 'default':
                page = menu_item[i].replace(" ","_")
                title = menu_item[i]
                form = "<form id='"+page+"-menu' action=''>"
                form += "<input type='hidden' id='page' name='page' value='"+page+"'>"
                form += title
                form += "</form>"
                print(f"<div class='menu_item {menu_item[i]}' onclick='document.getElementById(\"{page}-menu\").submit()'>{form}</div>")
        print(f"</div>")

    def print_css(self):
        print(f"<style>\n{self.css.replace('##PICTURE##',self.image)}\n</style>\n")

    def print_js(self):
        print(f"<script>\n{self.js}\n</script>\n")

    def print_items(self):
        print(f"<div class='content'>\n")
        from hasspyapi import hasspyapi
        for entity in self.items:
            #self.debug_append(len(entity))
            entity_id = entity[0]
            label_class = entity[1].replace(" ","_")
            onclick = entity[2]
            action = entity[3]
            domain = entity[4]
            hpa_status = hasspyapi([self.host,self.token,domain,"status",entity_id,self.logfile,self.debug])
            try:
                status = hpa_status.get_status()[1]
                self.debug_append(status)
            except:
                status = 'error'
            print(f"<div onclick='{onclick}' class='entity {label_class} {status}'>")
            print(f"<form method='post' id='{entity_id}' action='hasspyapi.cgi'>")
            print(f"<input type='hidden' name='token' id='token' value=\"{self.token}\">")
            print(f"<input type='hidden' name='host' id='host' value='{self.host}'>")
            print(f"<input type='hidden' name='debug' id='debug' value='{self.debug}'>")
            print(f"<input type='hidden' name='forward' id='forward' value='{self.forward}'>")
            print(f"<input type='hidden' name='entity' id='entity' value='{entity_id}'>")
            print(f"<input type='hidden' name='service' id='service' value='{action}'>")
            print(f"<input type='hidden' name='domain' id='domain' value='{domain}'>")
            print(f"{entity[1]}</div>")
            print("</form>")
    def print_footer(self):
        print("</div>\n</div>\n</body>\n<html>\n")

    def execute(self):
        if self.test == 'config_list':
            print("content-type: text/plain\n\n")
            print(self.get_config_list())
        else:
            self.get_config()
            self.get_items()
            self.print_header()
            if self.debugme:
                self.print_debug()
            else:
                self.print_menu()
                self.print_items()
            self.print_footer()

def main():
    hpd = hasspydisplay()
    hpd.execute()
main()