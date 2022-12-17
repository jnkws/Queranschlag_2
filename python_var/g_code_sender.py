#!/usr/bin/python

import serial
import time
import argparse
import param_server
import logging

class GCodeSender:
    def __init__(self, port) -> None:
        self.ser = serial.Serial(port=port, baudrate=param_server.baudRate)
        logging.info("Opening serial port")
        self.wakeUp()
    
    def wakeUp(self):
        self.ser.write(b"\r\n\r\n")
        time.sleep(2)
        while self.ser.inWaiting():
            print(self.ser.readline())
        self.ser.write(b"$$\n") # Hit enter a few times to wake the arduino
        time.sleep(2)   # Wait for arduino to initialize
        print(self.ser.inWaiting())
        while self.ser.inWaiting():
            print(self.ser.readline())
        self.ser.write(b"$X\n") # Hit enter a few times to wake the arduino
        time.sleep(2)   # Wait for arduino to initialize
        while self.ser.inWaiting():
            print(self.ser.readline())
        #print(self.ser.readlines(51))
        #self.ser.reset_input_buffer()  # Flush startup text in serial input
        print(self.ser.inWaiting())
       

    def send(self, cmd):
        self.ser.write(cmd)# + b'\n')
        time.sleep(2)
        while self.ser.inWaiting():
            print(self.ser.readline())
        # self.ser.write(b"$$\n") # Hit enter a few times to wake the arduino
        # time.sleep(2)   # Wait for arduino to initialize
        # print(self.ser.inWaiting())
        # while self.ser.inWaiting():
        #     print(self.ser.readline())
        #grblOut = self.ser.readline() # Wait for response with carriage return
        #logging.info(cmd + " : " + grblOut.strip())
        #logging.info(grblOut)

    def homePos(self):
        self.ser.write(b"G28\n")
        time.sleep(2)
        grblOut = self.ser.readline() # Wait for response with carriage return
        logging.info("G28 : " + grblOut.strip())

    def __del__(self):
        self.ser.close()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    sender = GCodeSender("COM8")
    sender.send(b"G01 F4000 X-50\n")
    print("HEllo")