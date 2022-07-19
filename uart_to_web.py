import time
import serial
import logging
import re
from tqdm import tqdm
from threading import Timer
from threading import Thread
from dataclasses import dataclass
from typing import ClassVar
from abc import ABC
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# new_coil = False
@dataclass
class CoilProperties:
    key: str = ""
    wnd_type: str = ""
    wnd_material: str = ""
    wnd_stop: str = ""
    prev_stop: str = ""
    coil_num: str = ""
    prev_coil_num: str = ""
    division: str = 1
    mat_width: str = ""
    stop_url: str = ""
    div_url: str = ""
    wnd_type_url: str = ""
    new_url: bool = True
    ignore_codes: ClassVar[list] = ["LE", "ALE", "TT", "ATT", "TS", "ATS", "TB", "ATB"]
    prev_msg: ClassVar[str] = ""
    base_url: ClassVar[
        str
    ] = "http://svr-webint1/WindingPractices/Home/Display?div=D{}&stop={}"
    startup_url: ClassVar[
        str
    ] = "http://svr-webint1/WindingPractices/Home/Display?div=D1&stop=NC"

    def __eq__(self, other):
        return self.wnd_stop == other.prev_stop

    def delete_coil(self):
        tempVar = self.coil_num
        self.__init__()
        self.prev_coil_num = tempVar
        return

    def show_coil(self):
        print(
            f"Coil Number: {self.coil_num}\n"
            + f"Division: {self.division}\n"
            + f"Winding: {self.wnd_type}\n"
            + f"Material: {self.wnd_material}\n"
            + f"Width: {self.mat_width}\n"
            + f"Code: {self.key}"
        )

    def set_stop_url(self):
        print("Stop to set: {}".format(self.wnd_stop))
        print("Prev Stop: {}".format(self.prev_stop))
        stop_prev = self.prev_stop
        if self.wnd_stop == stop_prev:
            # if any(target in self.wnd_stop for target in self.prev_stop):
            self.new_url = False
            print("URL DUPLICATE")
            return
        self.prev_stop = self.wnd_stop
        self.stop_url = self.base_url.format(self.division, self.wnd_stop)
        self.new_url = True
        return

    def set_wnd_type_url(self):
        self.wnd_type_url = self.base_url.format(self.division, self.wnd_type)
        return

    def set_div_url(self):
        self.div_url = self.base_url.format(self.division, "")
        return

    def edit_coil(self, uart_str):
        # region DocString
        """[summary]

        Args:
            uart_str ([str]): [Incoming Messages from Z80 over serial]

        Task:
            - Change particular attributes based on split uart_str items
            - Length == 4:
                EX: ['NW,HV,WC,00.1250']
                self.key = NW
                self.win_type = HV
                self.win_material = WC
                self.mat_width = 00.1250
                if self.win_material = WC
                    - lookup material and compare
                    - if material identified as aluminum or copper
                            self.wnd_stop = HVA # for aluminum
                            self.wnd_stop = HVC # for copper
                    - if no match:
                            self.wnd_stop = HV
                def set_stop_url()


            - Length == 3:
                EX: ['CI,0050123456789,1']
                if lst_data[0] == NC
                    - check if lst_data[1] == self.coil_num
                    True:
                        - continue with same instance of coil
                    False:
                        - use logging_info logger to export data to a txt file
                        - create a new instance of coilProperties
                            # possible ways for new instance
                            - use global variable
                            - reset attributes via a method
                            - call __init__
                self.key = CI
                self.coil_num = 00501234567889
                self.division = 1

            - Length is 1
                EX: ['AD'], ['CX'], ['DS'], ['LE'], ['FC']
                self.key = AD

                if self.key = 'FC'
                    -
        """
        # endregion
        # global new_coil
        if uart_str == self.prev_msg:
            self.new_url = False
            return

        self.prev_msg = uart_str
        lst_data = uart_str.split(",")
        list_len = len(lst_data)
        # print("List Length : {}".format(list_len))
        if any(target in ("RS") for target in lst_data):
            lst_data[0] = "DE"
            print("Changed 'RS' -> 'DE'")
            self.set_stop_url()
            return

            # self.wnd_type = lst_data[2]
            # self.wnd_material = lst_data[3]
            # self.mat_width = lst_data[4]
            # list_len=1
            # return

        # if lst_data[0] is "RS":
        #     self.wnd_stop = "DE"
        #     self.set_stop_url()
        #     return

        if list_len is 4:
            self.key = lst_data[0]
            self.wnd_type = lst_data[1]
            self.wnd_material = lst_data[2]
            self.mat_width = lst_data[3]
            self.wnd_stop = lst_data[1]
            self.set_stop_url()
            self.set_wnd_type_url()
            return

        if list_len is 3:
            if lst_data[1] == self.coil_num:
                # do nothing
                # this means the z80 was reset
                print("Coil is the same")
                self.new_url = False
                return
            self.delete_coil()
            self.key = lst_data[0]
            self.coil_num = lst_data[1]
            self.division = lst_data[2]
            self.set_div_url()
            self.wnd_stop = "NC"
            self.set_stop_url()
            print(
                "Deleted Coil: {}\n".format(self.prev_coil_num)
                + "Created Coil: {}".format(self.coil_num)
            )
            return True

        if list_len is 1:
            tmp_str = lst_data[0]
            print("Temp String: {}".format(tmp_str))
            str_len = len(tmp_str)
            print("String length: {}".format(str_len))
            if str_len == 4:
                self.wnd_stop = tmp_str[1:]
                print("Stop Code: {}".format(self.wnd_stop))
            else:
                self.wnd_stop = tmp_str

            if any(target in self.wnd_stop for target in self.ignore_codes):
                print("Code Ignored: {}".format(self.wnd_stop))
                self.new_url = False
                return
            self.set_stop_url()
            return True

        return False

    def log_coil(self):
        # logg stuff here, maybe move this out of the class,
        # i think theres a way to do this automatically
        # if i figure out how to close the class instance and create a new one
        # instead of using the __init__ method.
        pass

    # def get_url(self):
    #     x = "D1"
    #     y = "PA"
    #     return (
    #         # f"{self.base_url}"
    #         # + f"Div?={self.division}"
    #         # + f"/{self.dest_url}"
    #         self.base_url.format(x, y)
    #     )

    def get_hv_metal(self):
        pass


class ControlSerial:
    """[summary]

    Returns:
        [type]: [description]
    """

    ser = serial.Serial()
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = serial.EIGHTBITS
    ser.timeout = 1
    data = ""
    data_received = False
    filePath = Path("/home/pi/Desktop/Z80_Doc_Display.txt")

    # __INIT__
    #
    def __init__(self, port, baudrate):
        """__init__
        [Called by default everytime an
         instance of the class is created]
        [Most commonly changed args here]

        Args:
            port ([str]): [description]
            baudrate ([int]): [description]
        """
        self.port = port
        self.baudrate = baudrate

        self.filePath.touch(exist_ok=True)

        with (open(self.filePath, "a")) as fw0:
            fw0.write("----------------------------------")
            fw0.write(datetime.today().strftime("%Y-%m-%d" + "," "%H:%M:%S"))
            fw0.write("----------------------------------" + "\n")
            fw0.close()
        print(
            "Script Started: "
            + datetime.today().strftime("%Y-%m-%d" + "," "%H:%M:%S")
            + "\n"
        )
        # self.rx_msg = ""

    def open_port(self):
        self.ser.port = self.port
        self.ser.baudrate = self.baudrate
        if not self.ser.port:
            self.serial_error()
        # self.ser.open()
        # return 'Serial port {} succesffuly opened!'.format(self.port)
        try:
            self.ser.open()
            return "Serial port {} succesffuly opened!".format(self.port)
        except Exception as e:
            with (open(self.filePath, "a")) as fw1:
                fw1.write(str(e) + "<\n")
                fw1.close()
            print("Error: Serial Open " + str(e))
            self.ser.reset_input_buffer()
            return

    def close_port(self):
        self.ser.close()
        return "Serial port {} closed".format(self.port)

    def serial_error(self):
        return "Cannot open port {}".format(self.port)

    def read_serial(self):
        self.data_received = False
        while self.data_received is False:
            self.data = ""
            rx_data = self.ser.readline()
            utf8_data = rx_data.decode("utf8")

            if len(utf8_data) > 1:
                # print(utf8_data)
                self.data = utf8_data
                self.data_received = True
                self.log_serial()
        return

    def log_serial(self):
        with (open(self.filePath, "a")) as fw1:
            currentTime = datetime.today()
            # fw2.write(currentTime.strftime(
            #    '%H:%M:%S') + '>' + hex_data + '<\n')
            fw1.write(currentTime.strftime("%H:%M:%S") + ">" + self.data + "<")
            fw1.close()
        print(currentTime.strftime("%H:%M:%S") + ">  " + self.data + "<")
        return


def setup_webDriver():
    options = Options()
    options.add_argument("--kiosk")
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # driver = webdriver.Chrome(executable_path=r"/usr/bin/chromedriver")
    driver = webdriver.Chrome(options=options, executable_path=r"/usr/bin/chromedriver")
    return driver


def open_webpage(url, driver):
    try:
        driver.get("{}".format(url))
    except Exception as e:
        print("Selenium Erro: {}".format(e))
        return False
    # print(str(url))
    driver.implicitly_wait(2)
    check_error = driver.current_url

    if re.search("Error", check_error):
        element = driver.find_element_by_xpath("//h1")
        driver.execute_script(
            "arguments[0].innerText = 'Server Error in *WindingPractices* Application -- *****Program Message: Redirecting to [Most Relavent Directory] in 5 seconds....*****'",
            element,
        )
        time.sleep(5)
        # print(element.get_attribute('innerText'))
        driver.back()
        return False
    print(driver.current_url)
    return True


def main():
    uart = ControlSerial("/dev/ttyUSB0", 19200)
    uart.close_port()
    uart.open_port()

    coil = CoilProperties()
    coil.set_div_url()

    chrome = setup_webDriver()
    open_webpage(url=coil.startup_url, driver=chrome)
    # print(coil.ignore_codes)

    while True:
        uart.read_serial()
        # print(uart.data)
        coil.edit_coil(uart.data)
        if coil.new_url is True:
            if not open_webpage(url=coil.stop_url, driver=chrome):
                if not open_webpage(url=coil.wnd_type_url, driver=chrome):
                    open_webpage(url=coil.div_url, driver=chrome)

        # # if new_coil is True:
        # #     coil.__init__()  # Erase coil Data if 'FC' Code rx'd

        # # lst = uartString.split(",")
        # # print(len(lst))
        # # print(lst)

        # uartString = input("Enter Z80 string exactly: \n")
        # coil.edit_coil(uartString)
        # print(coil.stop_url)
        # if coil.new_url is True:
        #     open_webpage(url=coil.stop_url, driver=chrome)


if __name__ == "__main__":
    timer_duration = 0.5 * 60
    timer_expired = False

    def timer_expired_callback():
        global timer_expired
        print("Automatically restarting program...")
        timer_expired = True

    while True:
        try:
            timer_expired = False
            main()
        except Exception as e:
            print("Error: {}".format(e))
            with open("/home/pi/Desktop/cwid-error.log", "a") as fw:
                fw.write(str(e) + "\n")
                fw.close()
            threaded_timer = Timer(timer_duration, timer_expired_callback)
            threaded_timer.start()
            progressbar = tqdm(
                total=timer_duration,
                desc="Retrying in {} minutes...".format(timer_duration / 60),
                bar_format="{desc} {percentage:3.0f}%|{bar}|",
                leave=False,
            )

            while timer_expired is False:
                progressbar.update(1)
                time.sleep(1)
            if timer_duration <= 300:
                timer_duration *= 2
            progressbar.close()
            threaded_timer.cancel()
