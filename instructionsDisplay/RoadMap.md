# SQL DATA BASE RECORDS

<!-- Ignroe -->
- [SQL DATA BASE RECORDS](#sql-data-base-records)
  - [Databases](#databases)
    - [Table: Coil Winder Machines](#table-coil-winder-machines)
    - [Table: Coil Data by Machine](#table-coil-data-by-machine)

## Databases

### Table: Coil Winder Machines

| **ID** | **Division** |  **Hostname**  | **IP_Address** | **TYPE** | **Status** |  **Last_Seen**   |
| :----: | :----------: | :------------: | :------------: | :------: | :--------: | :--------------: |
|  001   |      0       | radjkw-mac-001 |  192.168.0.26  |   mac    |   Online   | (Last Ping Time) |
|  088   |      1       |  radpi-cw088   |  10.11.18.50   |  Raspi   |   Online   | (Last Ping Time) |

### Table: Coil Data by Machine

| id  |    number     | division | stop_code | layer | material |  width  |    rx_message    |                              web_url                              |      date_time      |            warnings            |
| :-: | :-----------: | :------: | :-------: | :---: | :------: | :-----: | :--------------: | :---------------------------------------36: | :-----------------: | :----------------------------: |
|  2  | 0987654321012 |    1     |    NW     |  HV   |    WC    | 00.0410 | NW,HV,WC,00.0410 | <http://svr-webint1/WindingPractices/Home/Display?div=D1&stop=HV> | 2022-06-24 12:45:09 |               []               |
|  3  | 0987654321012 |    1     |    FC     |  HV   |    WC    | 00.0410 |        FC        | <http://svr-webint1/WindingPractices/Home/Display?div=D1&stop=FC> | 2022-06-24 12:45:13 |               []               |
|  4  | 0987654321012 |    1     |    LE     |  HV   |    WC    | 00.0410 |        LE        | <http://svr-webint1/WindingPractices/Home/Display?div=D1&stop=FC> | 2022-06-24 12:45:16 | ['Message is an ignore code.'] |
