# -*- coding: utf-8 -*-
import os
import json
from pickle import NONE
import pprint
import socket
import questionary
from enum import Enum
from sql_controller import *
from coil_controller import CoilProperties
from mqtt_controller import MyMQTTClass


class Host(Enum):
    id = "001"
    name = socket.gethostname().split(".")[0]
    domain = socket.gethostname().split(".")[1]
    hostname =name + "-" + id    
    ipv4 = "192.168.0.26"


hostname = socket.gethostname().split(".")[0] + "+001"
hostname = hostname.split("+")
test_coil = CoilProperties()
uart_json_file = "instructionsDisplay/uart_messages.json"
uart_msg_dict = {}
uart_message = {"category": [], "layer": [], "payload": [], "test": False}
sql_connection = None
cw_data_table_name = "cw_{}_data".format(Host.id.value)
file_paths = {
    "uart_messages": "instructionsDisplay/uart_messages.json",
    "sql_database": "instructionsDisplay/coil_database.db",
}
database_tables = {
    "cw_machines": """ 
        CREATE TABLE IF NOT EXISTS cw_machines (
            id integer PRIMARY KEY,
            division text,
            hostname text,
            ip_addr text, type text,
            status text,
            last_seen datetime
        );""",
    f"{cw_data_table_name}": f"""
        CREATE TABLE IF NOT EXISTS {cw_data_table_name} (
            id integer PRIMARY KEY AUTOINCREMENT,
            number text ,
            division text ,
            stop_code text ,
            layer text ,
            material text,
            width text,
            rx_message text,
            web_url text,
            date_time datetime ,
            warnings text
        );""",
}
sql_host_dict = {"id": Host.id.value, "division": "1", "hostname" : Host.hostname.value, "ip_addr": Host.ipv4.value, "type": "mac", "status": "online", "last_seen": "2020-01-01"}

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, compact=False)


def load_json(file_name):
    with open(file_name) as json_file:
        json_data = json.load(json_file)
    return json_data


def get_message_from_user():
    _continue = True
    while _continue:  # run until user quits
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
                    choices=list(
                        uart_msg_dict["Winding Status"][uart_message["layer"][0]]
                    ),
                ).ask()
            )
        else:
            uart_message["payload"].append(
                questionary.select(
                    "Choose a Message :",
                    choices=uart_msg_dict[uart_message["category"][0]],
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
            test_message = ",".join(uart_message["payload"])
            test_coil_controller(test_coil, test_message)
            # test_mqtt_controller()

        _continue = questionary.confirm("Continue Testing", default=True).ask()

        if _continue:
            os.system("clear")
            print("Previous Message = {}".format(",".join(uart_message["payload"])))
            uart_message["category"].clear()
            uart_message["layer"].clear()
            uart_message["payload"].clear()
            uart_message["test"] = False


def test_coil_controller(coil, message):
    print("\nTesting Message = {}".format(message))
    coil.set_coil_properties(message)
    coil.get_instructions_url()
    pp.pprint(coil.__dict__())
    print("\n")
    sql_data = coil.__dict__()
    # TODO: use insert_data from sql_controller.py
    insert_data(sql_connection, f"{cw_data_table_name}", sql_data)
    return


def test_mqtt_controller(mqttc, message):
    # TODO: implement mqtt test
    pass


def main():
    print("Host = {}".format(Host.name.value + "-" + Host.id.value))
    for tables in database_tables:
        create_table(sql_connection, database_tables[tables])
    # insert sql_host_dict into cw_machines table
    insert_data(sql_connection, "cw_machines", sql_host_dict)
    get_message_from_user()
    sql_connection.close()


if __name__ == "__main__":
    # GLOBAL SCOPE
    os.system("clear")
    uart_msg_dict = load_json(file_paths["uart_messages"])
    sql_connection = create_conneciton(file_paths["sql_database"])
    main()
