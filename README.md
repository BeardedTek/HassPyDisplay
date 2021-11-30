# HassPyDisplay
![v0.2 Screenshot (11/29/2021)](/html/img/HassPyDisplay.png?raw=true "v0.2 Screenshot (11/29/2021")
* Uses the Home Assistant API to control entities within Home Assistant via web interface
* This is intended as a wall display (small 7" touchscreen device)
* Custom CSS can be included per page via json file

## Todo:
* ~~Get Current State for each entity~~
* Display Entity Attributes (maybe have a more info button): The API now pulls all the attributes and returns them in a list for status, just need to implement it in hasspydisplay.py
* Documentation Documentation Documentation
(Need to better comment the code at a minimum)
***
# Setup

Place contents of cgi-bin into apache2's cgi-bin location.  You can change this directory on Ubuntu by editing /etc/apache2/conf-enabled/serve-cgi-bin.conf

Place the rest in your html folder (/var/www/html by default on Ubuntu)
Must edit json/default.json at a minimum to start.
Follow the instructions therein

# ALPHA VERSION
This is VERY early stages.  If you have any input, please feel free to add an issue/pull request.

This was tested with Ubuntu 21.04 Server on a Raspberry Pi 4.

- The Bearded Tek
http://beardedtek.com
