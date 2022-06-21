from dataclasses import dataclass
from typing import ClassVar
import pprint
import os

os.system("clear")

# TODO: verify if Ignore Codes are working correctly

# TODO: write the main.py script to create a coil object and handle the logging
#   TODO: implement log to file each time a message is received
#   TODO: catalog data by coil number and division for logging


class CoilProperties:
    
    
    base_url: ClassVar[
        str
    ] = "http://svr-webint1/WindingPractices/Home/Display?div=D{division_number}&stop={instructions_code}"

    ignore_codes: ClassVar[list] = [
        ["LE", "ALE", "TT", "ATT", "TS", "ATS", "TB", "ATB"]
    ]

    def __init__(self):
        self.coil_number = None
        self.winding_layer = None
        self.winding_material = None
        self.material_width = None
        self.key = None
        self.coil_division = None
        self.return_url = None
        self.warning = []
        self.prev_message = None

    def __dict__(self):
        return {
            "info": {
                "message": self.prev_message,
                "warnings": self.warning,
                "url_address": self.return_url,
            },
            "data": {
                "coil_number": self.coil_number,
                "coil_division": self.coil_division,
                "winding_layer": self.winding_layer,
                "winding_material": self.winding_material,
                "material_width": self.material_width,
                "key": self.key,
            },
        }

    def assign_attributes(self, new_message):
        print(".... assigning attributes")
        
        self.warning = []
        if self.prev_message == new_message:
            self.warning.append(
                "Message is the same as previous new_message. Ignoring new_message."
            )
            return
        self.prev_message = new_message
        new_message = new_message.split(",")
        if len(new_message) == 1:
            for code in self.ignore_codes:
                if new_message[0] in code:
                    self.warning.append("Message is an ignore code. Ignoring new_message.")
                    return
            self.key = new_message[0]
        elif len(new_message) == 3:
            self.key = new_message[0]
            self.coil_number = new_message[1]
            self.coil_division = new_message[2]
            return

        elif len(new_message) == 4:
            self.winding_layer, self.key = new_message[1], new_message[1]
            self.winding_material = new_message[2]
            self.material_width = new_message[3]
            self.key = new_message[1]
            return
        else:
            self.warning.append("The new_message {new_message} is not a valid new_message. Please check the new_message and try again.".format(
                new_message=new_message
            ))
        return

    def build_url(self):
        print("....building URL\n")
        ## Check if self.coil_division is None
        if self.coil_division is None:
            self.warning.append("The Coil's Division is not set.")
            if self.return_url is None: 
                self.return_url = self.base_url.format(
                    division_number='', instructions_code=''
                )
            return

        # if self.warning contains more than 1 warning, pop the second warning
        if len(self.warning) > 1:
            self.warning.pop(1)

        self.return_url = self.base_url.format(
            division_number=self.coil_division, instructions_code=self.key
        )
        return
