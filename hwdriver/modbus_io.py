#!/usr/bin/python
# -*- coding: utf-8 -*-

from twisted.internet import reactor

try:
    from pymodbus.client.async import schedulers
    # from pymodbus.client.async.serial
    import AsyncModbusSerialClient
    from pymodbus.client.async.twisted
    import ModbusClientProtocol
except:
    from pymodbus.client.asynchronous import schedulers
    from pymodbus.client.asynchronous.serial import AsyncModbusSerialClient
    from pymodbus.client.asynchronous.twisted import ModbusClientProtocol

import time, json

import logging as log
import requests
# logging.basicConfig()
# log = logging.getLogger("pymodbus")
# log.setLevel(logging.DEBUG)
import threading
import time, sys

# ---------------------------------------------------------------------------#
# state a few constants
# ---------------------------------------------------------------------------#

SERIAL_PORT = "/dev/modbus"
CLIENT_DELAY = 0.1

mb_proto = None

push_cork = False
push_bottle = False

success = 1


class mb_unit(object):
    def __init__(self, iface):
        self.iface = iface
        self.events = dict()
        self.reset = False
        self.inited = False
        self.fcount = 0

    def error_handler(self, failure):
        """ Handle any twisted errors

        :param failure: The error to handle
        """
        log.error('PIZDEC!!!!!!')
        log.error(failure)
        # log.error('PIZDEC!!!!!!')
        # reactor.stop()
        # sys.exit(1)
        global proto
        proto.stop()


class mb_main(mb_unit):
    def __init__(self, iface):
        self.UNIT = 0xA1
        self.cork = push_cork
        self.bottle = push_bottle
        mb_unit.__init__(self, iface)

    def request(self):
        if not self.inited:
            log.warning('*** NOT INITED!')
            d = self.iface.read_holding_registers(0, 1, unit=self.UNIT)
            d.addCallbacks(self.init_response, self.error_handler)
        elif self.cork:
            self.bottle = False
            d = self.iface.write_registers(4, [0x1], unit=self.UNIT)
            d.addCallbacks(self.cork_response, self.error_handler)
        elif self.bottle:
            self.cork = False
            d = self.iface.write_registers(4, [0x2], unit=self.UNIT)
            d.addCallbacks(self.bottle_response, self.error_handler)
        else:
            d = self.iface.read_holding_registers(11, 3, unit=self.UNIT)
            d.addCallbacks(self.holding_response, self.error_handler)

    def holding_response(self, response):
        try:
            self.iface.rxed()
            try:
                if not self.cork and not self.bottle:
                    d = self.iface.read_holding_registers(11, 3, unit=self.UNIT)
                    d.addCallbacks(self.exit_response, self.error_handler)
            except:
                reactor.callLater(CLIENT_DELAY, self.iface.poll)
        except:
            log.exception('PENZEC READING HOLDER REGISTERS')

    def dummy_response(self, response):
        self.iface.rxed()
        reactor.callLater(CLIENT_DELAY, self.iface.poll)

    def init_response(self, response):
        self.iface.rxed()
        try:
            try:
                if response.getRegister(0) != 0xAB56:
                    log.error('BOARD %02X FAILED INIT, NO 0xAB56!=0x%04x' % (self.UNIT, response.getRegister(0)))
                else:
                    log.warning('BOARD HW IS READY')
                    self.inited = True
            except:
                log.exception('BOARD MAIN %02X FAILED INIT' % (self.UNIT))
        finally:
            reactor.callLater(CLIENT_DELAY, self.iface.poll)

    def cork_response(self, response):
        self.iface.rxed()
        try:
            self.cork = False
            time.sleep(2.0)
            d = self.iface.write_registers(4, [0x0], unit=self.UNIT)
            d.addCallbacks(self.exit_response, self.error_handler)
        except:
            log.exception('BOARD MAIN %02X FAILED CORK' % (self.UNIT))
            global proto
            proto.stop()

    def bottle_response(self, response):
        self.iface.rxed()
        try:
            self.bottle = False
            time.sleep(2.0)
            d = self.iface.write_registers(4, [0x0], unit=self.UNIT)
            d.addCallbacks(self.exit_response, self.error_handler)
        except:
            log.exception('BOARD MAIN %02X FAILED BOTTLE' % (self.UNIT))
            global proto
            proto.stop()

    def exit_response(self, response):
        self.iface.rxed()
        try:
            try:
                global success
                success = 0
                log.warning('*SUCCESS*')
                global proto
                proto.stop()
            except:
                log.exception('BOARD MAIN %02X FAILED EXIT' % (self.UNIT))
        finally:
            pass


class OurModbusProtocol(ModbusClientProtocol):

    def __init__(self, framer):
        """ Initializes our custom protocol

        :param framer: The decoder to use to process messages
        :param endpoint: The endpoint to send results to
        """
        ModbusClientProtocol.__init__(self, framer)
        log.debug("Beginning the processing loop")
        self.devlist = [mb_main(self)]
        self.curdev = self.devlist[0]
        self.to = False
        reactor.callLater(CLIENT_DELAY, self.poll)
        global mb_proto
        mb_proto = self

    def timed_out(self):
        try:
            self.to.cancel()
        except:
            pass
        self.transaction.delTransaction(-1)
        self.curdev.fcount += 1
        if self.curdev.fcount > 10:
            self.curdev.inited = False
            # self.curdev.gen_event('disconnected',timeout=0)
            # self.curdev.defer_event(False,'Timeout',501)
            global proto
            proto.stop()
        self.poll()

    def poll(self):
        try:
            try:
                self.to.cancel()
            except:
                pass
            nx = False
            nx_dev = self.devlist[0]
            for nn in self.devlist:
                if nn == self.curdev:
                    nx = True
                elif nx:
                    nx_dev = nn
                    break
            self.curdev = nx_dev

            self.to = reactor.callLater(1.5, self.timed_out)
            self.curdev.request()
        except:
            log.exception('ERROR IN POLL')

    def rxed(self):
        try:
            self.to.cancel()
        except:
            pass
        self.curdev.fcount = 0

    def reset(self):
        log.warning('RESET BOARDS!!!')
        for d in self.devlist:
            d.reset = True


if __name__ == "__main__":
    log.getLogger().setLevel(log.DEBUG)
    # log.getLogger().setLevel(log.WARNING)

    if len(sys.argv) > 1:
        push_bottle = (sys.argv[1] == 'bottle')
        push_cork = (sys.argv[1] == 'cork')

    import serial

    """
    proto, client = AsyncModbusSerialClient(schedulers.REACTOR,
                                            method="rtu", 
                                            port=SERIAL_PORT,
                                            xonxoff=False,
                                            rtscts=False,
                                            baudrate=57600,
                                            parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_TWO,
                                            bytesize=serial.EIGHTBITS,
                                            timeout=1.0, 
                                            proto_cls=OurModbusProtocol)
    proto.start()
    # proto.stop()
    """

    from pymodbus.client.sync import ModbusSerialClient

    import logging
    import logging.handlers as Handlers
    import sys, os, time

    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.INFO)

    UNIT = 0xA1

    log.warning('STARTING CLIENT')

    try:
        try:
            client = ModbusSerialClient(
                method="rtu",
                port=SERIAL_PORT,
                xonxoff=False,
                rtscts=False,
                baudrate=57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.EIGHTBITS,
                timeout=1.0)

            log.warning('SENDING COMMAND')

            rr = client.read_holding_registers(0, 1, unit=UNIT)
            if rr.registers[0] != 0xAB56:
                exit(success)
            rw = client.write_registers(4, [0], unit=UNIT)
            if push_bottle:
                rw = client.write_registers(4, [0x1], unit=UNIT)
            elif push_cork:
                rw = client.write_registers(4, [0x2], unit=UNIT)
            time.sleep(2.0)
            rw = client.write_registers(4, [0], unit=UNIT)
            log.warning('*SUCCESS*')
            success = 0
        except:
            log.exception('PENZEC!')
    finally:
        exit(success)
