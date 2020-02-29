import ctypes
import time
from serial import win32

# import serial
# from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError
from ft_serial import SerialBase

class Serial(SerialBase):
	BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800,
				 2400, 4800,9600, 19200, 38400, 57600, 115200)

	def __init__(self, *args, **kwargs):
		self._port_handle = None
		self._overlapped_read = None
		self._overlapped_write = None
		super(Serial, self).__init__(*args, **kwargs)

