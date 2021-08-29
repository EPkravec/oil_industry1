#!/usr/bin/python
# -*- coding: utf-8 -*-

from pihwdriver import PiGPIO
import tcp_device.chatserver

from twisted.internet import reactor, protocol, endpoints

from sgnlogger import init_log, log

GPIO = None

_modbus = False


class MGPIO(PiGPIO):
    pass


class XPubProtocol(tcp_device.chatserver.PubProtocol):

    def connectionLost(self, reason):
        global GPIO
        GPIO.terminate()
        tcp_device.chatserver.PubProtocol.connectionLost(self, reason)


class XPubFactory(tcp_device.chatserver.PubFactory):
    def buildProtocol(self, addr):
        return XPubProtocol(self)

    def connectionLost(self, reason):
        global GPIO
        GPIO.terminate()
        return tcp_device.chatserver.PubFactory.connectionLost(self, reason)


def merge_pipes(**named_pipes):
    import threading, Queue as queue
    # Constants. Could also be placed outside of the method. I just put them here
    # so the method is fully self-contained
    PIPE_OPENED = 1
    PIPE_OUTPUT = 2
    PIPE_CLOSED = 3

    # Create a queue where the pipes will be read into
    output = queue.Queue()

    # This method is the run body for the threads that are instatiated below
    # This could be easily rewritten to be outside of the merge_pipes method,
    # but to make it fully self-contained I put it here
    def pipe_reader(name, pipe):
        try:
            output.put((PIPE_OPENED, name,))
            try:
                for line in iter(pipe.readline, ''):
                    output.put((PIPE_OUTPUT, name, line.decode('utf8').rstrip(),))
            finally:
                output.put((PIPE_CLOSED, name,))
        except:
            log.failure('PIPE READER ERROR')

    # Start a reader for each pipe
    for name, pipe in named_pipes.items():
        t = threading.Thread(target=pipe_reader, args=(name, pipe,))
        t.daemon = True
        t.start()

    # Use a counter to determine how many pipes are left open.
    # If all are closed, we can return
    pipe_count = 0

    # Read the queue in order, blocking if there's no data
    for data in iter(output.get, ''):
        code = data[0]
        if code == PIPE_OPENED:
            pipe_count += 1
        elif code == PIPE_CLOSED:
            pipe_count -= 1
        elif code == PIPE_OUTPUT:
            yield data[1:]
        if pipe_count == 0:
            return


def cmb(arg=False):
    import subprocess, sys
    import commands
    import os.path
    succ = False
    cmd = 'python ' + os.path.dirname(__file__) + ('/modbus_io.pyc%s' % ((' %s' % arg) if arg else ''))
    log.warn(u'CMD: %s' % cmd)
    p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    for name, line in merge_pipes(out=p.stdout, err=p.stderr):
        log.warn(u'MODBUS SAYS: %s %s' % (name, line))
        if '*SUCCESS*' in line:
            succ = True
    return succ


def command_modbus(arg=False):
    try:
        return cmb(arg)
    except:
        log.failure(u'MODBUS ERROR, DISABLING')
        return False


def run_server(tcp_port="tcp:7000"):
    global GPIO
    log.warn(u'Запускаю сервер {tcp_port}',
             tcp_port=tcp_port
             )

    pf = XPubFactory()
    GPIO = MGPIO(pf)

    GPIO.has_modbus = _modbus

    @pf.command('STATUS', r'^STATUS$')
    def command_init(proto, args):
        # proto.sendLine('HELLO')
        GPIO.stateSend()

    @pf.command('LIGHT', r'^LIGHT\s+(on|off)$')
    def command_light(proto, args):
        GPIO.light = True if args.group(1) == 'on' else False

    @pf.command('BOTTLE', r'^BOTTLE\s+(open|close|sell)$')
    def command_bottle(proto, args):
        if _modbus:
            command_modbus('bottle')
        if args.group(1) == 'sell':
            GPIO.sellBottle()
        else:
            GPIO.mag_bottle = True if args.group(1) == 'open' else False

    @pf.command('CORK', r'^CORK\s+(open|close|sell)$')
    def command_cork(proto, args):
        if _modbus:
            command_modbus('cork')
        if args.group(1) == 'sell':
            GPIO.sellBottle()
        else:
            GPIO.mag_bottle = True if args.group(1) == 'open' else False

    @pf.command('DOOR', r'^DOOR\s+(open|close)$')
    def command_door(proto, args):
        if args.group(1) == 'open':
            GPIO.setDoorLock(False)
        else:
            GPIO.setDoorLock(True)

    @pf.command('PUMP', r'^PUMP\s+([0-9]+|stop|pause|continue)\s*(WASH)?\s*(CALIB)?$')
    def command_pump(proto, args):
        GPIO.wash = (args.group(2) == 'WASH')
        GPIO.calib = (args.group(3) == 'CALIB')
        if args.group(1) == 'pause':
            GPIO.setPumpPause(True)
        elif args.group(1) == 'continue':
            GPIO.setPumpPause(False)
        elif args.group(1) == 'stop':
            GPIO.setPulseCounter(0)
        else:
            GPIO.setPulseCounter(int(args.group(1)))

    @pf.command('MINPULSES', r'^MINPULSES\s+([0-9]+)$')
    def command_minpulses(proto, args):
        GPIO.setMinPulses(int(args.group(1)))

    @pf.command('EMULATE', r'^EMULATE\s+(on|off)$')
    def command_emulate(proto, args):
        GPIO.emulation = True if args.group(1) == 'on' else False

    @pf.command('KEY', r'^KEY\s+([1-8])$')
    def command_key(proto, args):
        GPIO.notifyKeyDown(int(args.group(1)))

    endpoints.serverFromString(reactor, tcp_port).listen(pf)

    reactor.run()

    if GPIO:
        GPIO.terminate()


if __name__ == '__main__':

    init_log(__file__)

    log.warn('STARTING...')

    import yaml

    try:
        config = '/etc/kiosk/devices.yaml'
        f = open(config, "r")
        cfg = yaml.load(f)
        f.close();
    except:
        log.failure("Cannot read %s" % config)

    try:
        p = "tcp:%s" % cfg['devices']['HwDriver']['tcp_port']
    except:
        p = False

    log.warn('DEVICE CONFIG READY %s %s' % (p, config))

    # import huid
    # huid.CUSTOMERlog('SERIVCE_HW_STARTED',(huid.versionOf('hwdriver')))

    if command_modbus():
        log.warn('MODBUS CONTROLLER FOUND')
        _modbus = True
    else:
        _modbus = False
        log.error('* MODBUS CONTROLLER NOT FOUND')

    log.warn('READY TO START')

    try:
        if p:
            run_server(p)
        else:
            run_server()
    except:
        log.failure("RUNTIME ERROR")

    if GPIO:
        GPIO.terminate()
