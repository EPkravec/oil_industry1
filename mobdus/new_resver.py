#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import threading

import serial
from pymodbus.client.sync import ModbusSerialClient
import time
from pymodbus.bit_read_message import ReadBitsRequestBase

FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)


class InfoClaveModbusoil():

    def __init__(self):
        self.unit = 0xA1
        self.port = '/dev/ttyUSB0'
        self.method = "rtu"
        self.baudrate = 57600

    def coonect_port_slave(self):
        try:
            client = ModbusSerialClient(
                method=self.method,
                port=self.port,
                xonxoff=False,
                rtscts=False,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.EIGHTBITS,
                timeout=1.0)

            logging.info('Подключаемся к порту - %s' % self.port)
            client.connect()
            if not client.connect():
                logging.info('Не смогли подключиться к порту - %s' % self.port)
            else:
                logging.info('Подключились к порту - %s' % self.port)
                return client
        except:
            logging.info('Не смогли запустить программу')

    def poll(self):
        slave = self.coonect_port_slave()
        time.sleep(2)
        mini = slave.read_holding_registers(13, 1, unit=self.unit)
        if not mini.isError():
            logging.info('Получен ответ slave.registers = %s' % mini.registers)

            print(len(mini.registers))
        else:
            logging.info('Получен ответ c ошибкой slave = %s' % mini)
        # maxi = slave.read_coils(self.unit, 2)
        # # slave.report_slave_id(1)
        # # logging.info('Получен ответ slave.registers - %s' % maxi.register)
        # logging.info('Получен ответ slave.registers - %s' % maxi)
        # return  maxi

    # def respose_decode(self):
    #     ReadBitsRequestBase


def run_reser():
    slave = InfoClaveModbusoil()
    # slave.coonect_port_slave()
    slave.poll()


if __name__ == '__main__':
    while True:
        go = threading.Thread(target=run_reser)
        go.start()
        time.sleep(7)
