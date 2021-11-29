#!/usr/bin/python
import cgi
input = cgi.FieldStorage()
if input.getvalue('json') != None:
    json_input = "/var/www/html/json/"+input.getvalue('json')+".json"
else:
    json_input = "/var/www/html/json/default.json"
def config_json():
    import json
    with open(json_input) as json_file:
        data = json.load(json_file)
        for key in data:
            if key == "config":
                config = data[key]
                token = config['token']
                host = config['host']
                debug = config['debug']
                forward = config['forward']
                css = config['css']
                js = config['js']
                print("content-type: text/html\n\n")
                print(f"<html>\n<head>\n<style>")
                css_file = open(css)
                print(css_file.read())
                print(f"</style>")
                print(f"<script src='{js}'></script>")
                print("</head>\n<body>")
            else:
                entity = data[key]
                entity_id = entity['entity']
                onclick = "document.getElementById(\""+entity_id+"\").submit()"
                print(f"<form method='post' id='{entity_id}' action='ha_api.cgi'>\n")
                print(f"<input type='hidden' name='token' id='token' value=\"{token}\">\n")
                print(f"<input type='hidden' name='host' id='host' value='{host}'\n>")
                print(f"<input type='hidden' name='debug' id='debug' value='{debug}'>")
                print(f"<input type='hidden' name='forward' id='forward' value='{forward}'>\n")
                print(f"<input type='hidden' name='entity' id='entity' value='{entity['entity']}'>\n")
                print(f"<input type='hidden' name='service' id='service' value='{entity['action']}'>\n")
                print(f"<input type='hidden' name='domain' id='domain' value='{entity['domain']}'>\n")
                print(f"<div onclick='{onclick}' class='entity {key}''>{key}</div>\n")
                print("</form>\n\n")
                #for key in entity:
                #    print(key, ' : ', entity[key])
                print("\n")
        print("</body>\n</html>")
def main():
    
    config_json()
main()