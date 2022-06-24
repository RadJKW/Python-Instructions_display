import sqlite3
from sqlite3 import Error

database_tables = {}


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

    #

    return conn


def create_table(conn, create_sql_table, host_id=None):
    """create a table from the create_sql_table statement
    :param conn: Connection object
    :param create_sql_table: a CREATE TABLE statement
    :return:
    """
    if host_id is not None:
        create_sql_table = create_sql_table.format(host_id)

    try:
        c = conn.cursor()
        c.execute(create_sql_table)
    except Error as e:
        print(e)


def build_sql_script(data):
    """builds a sql script from the data dictionary.
    :param data: coil data
    :return: sql data
    """


def insert_data(conn, sql_table, sql_data):
    """
    :param conn: Connection object
    :param sql_table: table name
    :param sql_data: data to be inserted
    :return:
    """
    # If the dictionary keys are coulumn names, and the values are the data to be inserted
    # then we can use the dictionary directly.
    # if the value of a key is a string, then we need to wrap it in quotes.

    sql_data_keys = sql_data.keys()
    sql_data_values = sql_data.values()
    sql_data_values = [str(value) for value in sql_data_values]
    sql_data_values = [value.replace("'", "''") for value in sql_data_values]
    sql_data_values = [f"'{value}'" for value in sql_data_values]
    sql_data_values = ",".join(sql_data_values)
    sql_data_keys = ",".join(sql_data_keys)
    sql_data_keys = f"({sql_data_keys})"
    sql_data_values = f"({sql_data_values})"
    sql_insert_statement = (
        f"INSERT INTO {sql_table} {sql_data_keys} VALUES {sql_data_values}"
    )
    try:
        c = conn.cursor()
        c.execute(sql_insert_statement)
        conn.commit()
    except Error as e:
        print(e)

    # sql = """ INSERT INTO CW_001_DATA (number,division,stop_code,layer,material,width,rx_message,web_url,date_time,warnings) VALUES("{number}",{division},"{stop_code}","{layer}","{material}",{width},"{rx_message}","{web_url}","{date_time}","{warnings}") """.format(
    #     number=sql_data["number"],
    #     division=sql_data["division"],
    #     stop_code=sql_data["stop_code"],
    #     layer=sql_data["layer"],
    #     material=sql_data["material"],
    #     width=sql_data["width"],
    #     rx_message=sql_data["rx_message"],
    #     web_url=sql_data["web_url"],
    #     date_time=sql_data["date_time"],
    #     warnings=",".join(sql_data["warnings"]),
    # # )
    # cur = conn.cursor()
    # cur.execute(sql_insert_statement)
    # conn.commit()
