import serial

from ft_serial_1 import *

ser_1 = Serial('COM3')
ser_2 = Serial('COM4')
ser_1.write(b"H\n")
data_to_read = ser_2.in_waiting
if data_to_read > 0:
	line = ser_2.read(data_to_read)
	print(line)
ser_2.write("Yeah, Hello\r\n".encode('utf-8'))
data_to_read = ser_1.in_waiting
if data_to_read > 0:
	line = ser_1.read(data_to_read)
	print(line)