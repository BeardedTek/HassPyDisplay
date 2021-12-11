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

class hasspyconfig:
    def __init__(self,config_file):
        self.config_file = "../.config/config.json"
        self.config = self.get_config(self,config_file)
        self.debug=[]
        return self.config
    
    def get_config(self,config_file):
        try:
            import json
            with open(config_file) as json_data:
                output = json.load(json_data)
        except:
            output = {"config":{"get_config":f"Cannot Get Config from {config_file}."}}
        finally:
            return output
    
    def write_config(self,config_data):
        # Make sure config_data is a dictionary
        if type(config_data) is dict:
            import json
            # Make a backup copy of the last configuration (Just in case)
            from shutil import copyfile
            backup=self.config_file+"~"
            copyfile(self.config, backup)
            # Write the configuration data to file
            with open(self.config_file,"w") as outfile:
                json.dump(config_data, outfile)
            return {"conf":{"write_config":"OK"}}
        else:
            return {"conf":{"write_config":"Input not a dictionary"}}

