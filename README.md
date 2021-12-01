# HassPyDisplay
![v0.3.1](/html/img/hasspydisplay.png)
* Uses the Home Assistant API to control entities within Home Assistant via web interface
* This is intended as a wall display (small 7" touchscreen device)
* Custom CSS can be included per page via json file
### Todo:
* ~~Get Current State for each entity~~
* ~~Generate menu from contents of the json directory~~
* Display Entity Attributes (maybe have a more info button): The API now pulls all the attributes and returns them in a list for status, just need to implement it in hasspydisplay.py
* Documentation Documentation Documentation
(Need to better comment the code at a minimum)
***
## Setup
* Place contents of cgi-bin into apache2's cgi-bin location.
* Place the rest in your html folder
* Edit example.json, rename it to title of menu item and place in html/json directory
* Filename dictates menu item name #CHANGEME#
### example.json:
```
{
    "config":{
        "token": "YOUR HA Long Lived Access Token",
        "host": "http(s)://homeassistant.local:8123",
        "logfile": "/var/log/hasspydisplay",
        "forward": "hasspydisplay.py?page=example.json",
        "image": "../img/home_front.webp",
        "css": "../css/ha_display.css",
        "js": "../js/ha_display.js"
    },
    "Driveway":{
        "entity": "light.driveway_lights",
        "domain": "light",
        "action": "toggle"
    },
    "Garage":{
        "entity": "light.garage_lights",
        "domain": "light",
        "action": "toggle"
    },
    "Open Garage Door":{
        "entity": "input_boolean.garage_door_open",
        "domain": "input_boolean",
        "action": "turn_on"
    },
    "Close Garage Door":{
        "entity": "input_boolean.garage_door_close",
        "domain": "input_boolean",
        "action": "turn_on"
    }
}
```

- The Bearded Tek
http://beardedtek.com