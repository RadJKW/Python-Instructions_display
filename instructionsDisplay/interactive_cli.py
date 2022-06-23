# -*- coding: utf-8 -*-
import os
import json
from pickle import NONE
import pprint
import socket
import sqlite3
from sqlite3 import Error
import questionary
from enum import Enum
from coil_controller import CoilProperties
from mqtt_controller import MyMQTTClass


class Host(Enum):
    id = "001"
    name = socket.gethostname().split(".")[0]
    domain = socket.gethostname().split(".")[1]
    ipv4 = "192.168.0.26"


hostname = socket.gethostname().split(".")[0] + "+001"
hostname = hostname.split("+")
test_coil = CoilProperties()
uart_json_file = "instructionsDisplay/uart_messages.json"
uart_msg_dict = {}
uart_message = {"category": [], "layer": [], "payload": [], "test": False}
sql_connection = None
cw_data_table = "cw_{}_data".format(Host.id.value)
file_paths = {
    "uart_messages": "instructionsDisplay/uart_messages.json",
    "sql_database": "instructionsDisplay/coil_database.db",
}
database_tables = {
    "cw_machine": """ 
        CREATE TABLE IF NOT EXISTS cw_machine (
            id integer PRIMARY KEY,
            division integer,
            hostname text,
            ip_addr text, type text,
            status text,
            last_seen text
        );""",
    "{}".format(
        cw_data_table
    ): """
        CREATE TABLE IF NOT EXISTS {} (
            id integer PRIMARY KEY AUTOINCREMENT,
            number integer ,
            division integer ,
            stop_code text ,
            layer text ,
            material text,
            width decimal(6,2),
            message text,
            url text,
            date_time datetime,
            warning text
        );""".format(
        cw_data_table
    ),
}
pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, compact=False)


def load_json(file_name):
    with open(file_name) as json_file:
        json_data = json.load(json_file)
    return json_data


def create_conneciton(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_sql_table):
    """create a table from the create_sql_table statement
    :param conn: Connection object
    :param create_sql_table: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_sql_table)
    except Error as e:
        print(e)


def get_message_from_user():
    _continue = True
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
    append_sql_database(sql_connection, "CW_{}_DATA".format(Host.id.value), sql_data)
    return


def append_sql_database(conn, sql_table, sql_data):
    """
    :param conn: Connection object
    :param sql_table: table name
    :param sql_data: data to be inserted
    :return:
    """

    print(sql_data)
    sql = """ INSERT INTO CW_001_DATA (number,division,stop_code,layer,material,width,message,url,date_time,warning) VALUES({number},{division},"{stop_code}","{layer}","{material}",{width},"{message}","{url}","{date_time}","{warnings}") """.format(
        number=sql_data["coil_number"],
        division=sql_data["coil_division"],
        stop_code=sql_data["stop_code"],
        layer=sql_data["winding_layer"],
        material=sql_data["winding_material"],
        width=sql_data["material_width"],
        message=sql_data["z80_output"],
        url=sql_data["url_address"],
        date_time=sql_data["date_time"],
        warnings=",".join(sql_data["warnings"]),
    )

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def test_mqtt_controller(mqttc, message):
    pass


def main():
    print("Host = {}".format(Host.name.value + "-" + Host.id.value))
    for tables in database_tables:
        create_table(sql_connection, database_tables[tables])
    get_message_from_user()
    sql_connection.close()


if __name__ == "__main__":
    # GLOBAL SCOPE
    os.system("clear")
    uart_msg_dict = load_json(file_paths["uart_messages"])
    sql_connection = create_conneciton(file_paths["sql_database"])
    main()
