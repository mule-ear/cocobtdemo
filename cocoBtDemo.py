#!/usr/bin/env python3
from tkinter import *
import bluetooth, sys, time

import configparser, logging, argparse

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
# Had to make sock global - workaround because it kept disconnecting
# when it was part of the bt_connect function
# If I run across a better way, I'll fix this

'''gui.py was written specifically for an arduino/bluetooth demo
Pretty much everything is hard coded, excpet the bluetooth address.
This is not meant to be robust, more of a POC.
But it's meant to be easily expandable. 
Logging and configparser are already started.
Maybe I'll add a simple argparse in the spirit of keeping it easy
to alter/expand upon.
'''

def getConfig():
    config =configparser.ConfigParser()
    config.read('bt.cfg')
    return (config['Main']['address'], config['Main']['port'], config['Main']['timeout'])

def setUpLogger():
    
    if sys.platform == "linux":
        formatter=logging.Formatter('\033[1;33m%(asctime)s,%(msecs)d \033[1;34m %(name)s \033[0;36m%(levelname)s \033[0;32m%(message)s \033[m', datefmt='%H:%M:%S')
    else:
        formatter=logging.Formatter('%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')

    logger = logging.getLogger('Bluetooth_CoCo_Demo')
    logger.setLevel(logging.DEBUG)

    # log to file
    fh = logging.FileHandler("/tmp/bluetooth_cocoDemo.log")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # log to stderr
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger

def getCLIArguments(bt_addr):

    parser = argparse.ArgumentParser(description = "Simple interface forbluetooth communication to a simple arduino program.")
    # Optional bluetooth address
    parser.add_argument("address", nargs = '?', default=bt_addr, help = "Specify HC-06 module address")
    # Optional log level
    parser.add_argument("-l","--log-level",default="DEBUG")
    args = parser.parse_args()
    return (args.address, args.log_level)

def btConnect( sock, btAddr, btPort, bt_timeout):
    log.info("Trying to connect "+ btAddr)
    try:
        #sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect(( btAddr, btPort))
        #sock.settimeout(bt_timeout)
        # test -> sock.send("4")
    except bluetooth.btcommon.BluetoothError as e:
        log.error("Caught an exception connecting:"+ str(e))
        sys.exit(22)
    else:
        log.debug("Successful ?")

def ledOn(sock):
    try:
        log.debug("Turning the LED on")
        sock.send("1")
    except bluetooth.btcommon.BluetoothError as e:
        log.error("Caught an exception connecting:"+ str(e))
        log.error("You may need to connect first")
        return
    log.info(sock.recv(3))

def ledOff():
    try:
        log.debug("Turning the LED off")
        sock.send("0")
        log.info(sock.recv(2))
    except bluetooth.btcommon.BluetoothError as e:
        log.error("Caught an exception connecting:"+ str(e))
        log.error("You may need to connect first")
        return

def runSubroutine():
    try:
        log.debug("Running the test subroutine")
        sock.send("2")
    except bluetooth.btcommon.BluetoothError as e:
        log.error("Caught an exception connecting:"+ str(e))
        log.error("You may need to connect first")
        return

def relayOn():
    try:
        log.debug("Activating relay")
        sock.send("3")
    except bluetooth.btcommon.BluetoothError as e:
        log.error("Caught an exception connecting:"+ str(e))
        log.error("You may need to connect first")
        return

def relayOff():
    try:
        log.debug("De-activating the relay")
        sock.send('4')
    except bluetooth.btcommon.BluetoothError as e:
        log.error("Caught an exception connecting:"+ str(e))
        log.error("You may need to connect first")
        return

def creatGui( addr, port, timeout, sock ):
    win = Tk()
    win.wm_title("CoCo Bluetooth Demo")
    log.info("Creating window")
    b0 = Button(win, text = "Connect", command = lambda: btConnect(sock, addr, int(port), int(timeout))).pack(side=LEFT)
    b1 = Button(win, text = "LED on", command = lambda: ledOn(sock)).pack(side=LEFT)
    b2 = Button(win, text = "LED off", command = ledOff).pack(side=LEFT)
    b3 = Button(win, text = "Run subroutine", command = runSubroutine).pack(side=LEFT)
    b4 = Button(win, text = "Relay on", command = relayOn).pack(side=LEFT)
    b5 = Button(win, text = "Relay off", command = relayOff).pack(side=LEFT)
    b6 = Button(win, text = "Quit", command = win.destroy).pack(side=LEFT)

    return win

if __name__ == "__main__":

    bt_addr,port,timeout = getConfig()
    # Adding in sinmple loggers, both file and stderr
    addr, log_level = getCLIArguments(bt_addr)
    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError("Invalid log level")
    log = setUpLogger()
    log.setLevel(numeric_log_level)

    log.info("Starting up...")
    win = creatGui(addr, port, timeout, sock)
    win.mainloop()

