# CWID - Becoming Production Ready

<!-- Ignroe -->

- [SQL DATA BASE RECORDS](#sql-data-base-records)
  - [Databases](#databases)
    - [Table: Coil Winder Machines](#table-coil-winder-machines)
    - [Table: Coil Data by Machine](#table-coil-data-by-machine)
  - [Todo List:](#todo-list)
    - [](#)

## Databases

### Table: Coil Winder Machines

| **ID** | **Division** |  **Hostname**  | **IP_Address** | **TYPE** | **Status** |  **Last_Seen**   |
| :----: | :----------: | :------------: | :------------: | :------: | :--------: | :--------------: |
|  001   |      0       | radjkw-mac-001 |  192.168.0.26  |   mac    |   Online   | (Last Ping Time) |
|  088   |      1       |  radpi-cw088   |  10.11.18.50   |  Raspi   |   Online   | (Last Ping Time) |

### Table: Coil Data by Machine

| id  |    number     | division | stop_code | layer | material |  width  |    rx_message    |  web_url  |      date_time      | warnings |
| :-: | :-----------: | :------: | :-------: | :---: | :------: | :-----: | :--------------: | :-------: | :-----------------: | :------: |
|  2  | 0987654321012 |    1     |    NW     |  HV   |    WC    | 00.0410 | NW,HV,WC,00.0410 | "WEB_URL" | 2022-06-24 12:45:09 |          |
|  3  | 0987654321012 |    1     |    FC     |  HV   |    WC    | 00.0410 |        FC        | "WEB_URL" | 2022-06-24 12:45:13 |          |
|  4  | 0987654321012 |    1     |    LE     |  HV   |    WC    | 00.0410 |        LE        | "WEB_URL" | 2022-06-24 12:45:16 |          |

## System Architecture

### Python Code Development

> - Requirements...
>   - read serial data from z80
>   - open web browser to instructions
> - Added Features...
>   - CRUD operations for database
>   - MQTT publish?
>   - Better Logging
>   - New Test created (interactive_cli.py)

### Flutter - Instructions Viewer

> - Requirements...
>   - Display PDF / Video to user
>   - Manual / Automatic browsing
>   - Dynamically use updated instructions from server

### Flutter - Dashboard / Database Browser

> - Requirements...
>   - View Real Time data of all coil_winder machines.
>   - Allow user to query database with GUI's
>   - Clean and simple visualizations
>   - Imformative

### ASP Dotnet WEB_API

> - Requrements...
>   - Middleman between flutter and MS SQL Server
>   - Endpoints TBD.
