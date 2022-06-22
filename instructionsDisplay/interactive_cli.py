# -*- coding: utf-8 -*-
import os
import json
import pprint
import socket
import questionary
from coil_controller import CoilProperties
from mqtt_controller import MyMQTTClass

# TODO: implement log to file

#region -------------------    GLOBAL INIT      ----------------------------
os.system("clear")

hostname = socket.gethostname()
hostname = hostname.split(".")[0]
test_coil = CoilProperties()
_continue = True

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, compact=False)

uart_msg_dict = {}
with open("instructionsDisplay/uart_messages.json") as json_file:
    uart_msg_dict = json_data = json.load(json_file)
uart_string = []
uart_message = {"category": [], "layer": [], "payload": [], "test": False}

# endregion -------------------------------------------------------------------

#region -------------------    FUNCTIONS      ----------------------------
def test_coil_controller():
    test_message = ",".join(uart_message["payload"])
    print("Testing Message = {}".format(test_message))
    test_coil.set_coil_properties(test_message)
    test_coil.get_instructions_url()
    pp.pprint(test_coil.__dict__())
    # coil.set_coil_properties(message)
    # print("Testing Message = {}".format(message))
    # coil.get_instructions_url()
    # pp.pprint(coil.__dict__())
    # return

def test_mqtt_controller(mqttc, message):
    pass

# endregion -------------------------------------------------------------------

while _continue:
    uart_message["category"].append(
        questionary.select("Message Type:", choices=list(uart_msg_dict)).ask()
    )

    if uart_message["category"][0] == "Winding Status":
        # append the uart_message["layer"] list with the items in the uart_msg_dict["Winding Status"] list
        uart_message["layer"].append(
            questionary.select(
                "Winding Layer:", choices=list(uart_msg_dict["Winding Status"])
            ).ask()
        )
        uart_message["payload"].append(
            questionary.select(
                # present the user with list of items under each key in the uart_msg_dict["Winding Status"] dict
                "Winding Status:",
                choices=list(uart_msg_dict["Winding Status"][uart_message["layer"][0]]),
            ).ask()
        )
    else:
        uart_message["payload"].append(
            questionary.select(
                "Choose a Message :", choices=uart_msg_dict[uart_message["category"][0]]
            ).ask()
        )

    uart_message["test"] = questionary.confirm(
        "Test this UART Message? \n {payload}".format(
            payload=",".join(uart_message["payload"])
            # questionary.print(",".join(uart_message["payload"]), style='bold italic fg:red')
        ),
        default=True,
    ).ask()

    if uart_message["test"]:
        # test_message = ",".join(uart_message["payload"])
        # test_coil_controller(test_coil, test_message)
        test_coil_controller()
        #test_mqtt_controller()
        
        
        

    _continue = questionary.confirm("Continue Testing", default=True).ask()

    if _continue:
        os.system("clear")
        print("Previous Message = {}".format(",".join(uart_message["payload"])))
        uart_message["category"].clear()
        uart_message["layer"].clear()
        uart_message["payload"].clear()
        uart_message["test"] = False


