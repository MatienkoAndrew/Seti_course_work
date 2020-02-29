#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
# import serial
#from tkinter import *
from ft_serial_1 import *

# ser = serial.Serial('COM1')
ser = Serial('COM1')
if not ser:
	print("BAD")
