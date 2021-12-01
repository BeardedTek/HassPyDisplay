# HassPyDisplay
![v0.3.1](/html/img/hasspydisplay.png)
* Uses the Home Assistant API to control entities within Home Assistant via web interface
* This is intended as a wall display (small 7" touchscreen device)
* Custom CSS can be included per page via json file

## Todo:
* ~~Get Current State for each entity~~
* ~~Generate menu from contents of the json directory~~
* Display Entity Attributes (maybe have a more info button): The API now pulls all the attributes and returns them in a list for status, just need to implement it in hasspydisplay.py
* Documentation Documentation Documentation
(Need to better comment the code at a minimum)
***
# Setup

Place contents of cgi-bin into apache2's cgi-bin location.  You can change this directory on Ubuntu by editing /etc/apache2/conf-enabled/serve-cgi-bin.conf

* Place the rest in your html folder (/var/www/html by default on Ubuntu)
* Rename default.json as it is ignored.
* Filename dictates menu item name #CHANGEME#
Follow the instructions therein

# ALPHA VERSION
This is VERY early stages.  If you have any input, please feel free to add an issue/pull request.

This was tested with Ubuntu 21.04 Server on a Raspberry Pi 4.

- The Bearded Tek
http://beardedtek.com