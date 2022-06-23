import os
import datetime
from typing import ClassVar

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
        self.coil_division = None
        self.winding_layer = None
        self.winding_material = None
        self.material_width = None
        self.url_stop = None        
        self.web_url = None
        self.warning = []
        self.prev_message = None
        self.date_time = None
        self.stop_code = None

    def __dict__(self):
        return_dict = {
            #return self."item" if self."item" is not None else "None"
            "coil_number": self.coil_number,
            "coil_division": self.coil_division,
            "stop_code": self.stop_code,
            "winding_layer": self.winding_layer,
            "winding_material": self.winding_material,
            "material_width": self.material_width,
            "z80_output": self.prev_message,
            "url_address": self.web_url,
            "date_time": self.date_time,            
            "warnings": self.warning,
        } 
        for key in return_dict:
            if return_dict[key] is None:
                if key == "coil_number":
                    return_dict[key] = 0
                elif key == "coil_division":
                    return_dict[key] = 0
                elif key =="material_width":
                    return_dict[key] = 00.00
                else:
                    return_dict[key] = "None"
        return return_dict
    def set_coil_properties(self, new_message):
        print("....assigning attributes")
        self.warning = []
        self.date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.prev_message == new_message:
            self.warning.append(
                "Message is the same as previous new_message. Ignoring new_message."
            )
            return
        self.prev_message = new_message
        new_message = new_message.split(",")

        if len(new_message) == 1:
            self.stop_code = new_message[0]
            if new_message[0] in self.ignore_codes[0]:
                self.warning.append("Message is an ignore code.")
            else:
                self.url_stop = new_message[0]
            return

        if len(new_message) == 3:
            self.url_stop = new_message[0]
            self.stop_code = new_message[0]
            self.coil_number = new_message[1]
            self.coil_division = new_message[2]
            return

        if len(new_message) == 4:
            self.stop_code = new_message[0]
            self.url_stop = new_message[1]
            self.winding_layer = new_message[1]
            self.winding_material = new_message[2]
            self.material_width = new_message[3]
            return

        self.warning.append("Message is not a valid message.")

    def get_instructions_url(self):
        print("....building URL\n")
        ## Check if self.coil_division is None
        if self.coil_division is None:
            self.warning.append("The Coil's Division is not set.")
            if self.web_url is None:
                self.web_url = self.base_url.format(
                    division_number="", instructions_code=""
                )
            return

        self.web_url = self.base_url.format(
            division_number=self.coil_division, instructions_code=self.url_stop
        )
        return


# class CoilID(CoilProperties):
