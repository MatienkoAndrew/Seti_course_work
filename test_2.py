import serial

ser_1 = serial.Serial('COM3')
ser_2 = serial.Serial('COM4')

ser_1.write("Hello\r\n".encode('utf-8'))
line = ser_2.readline()
if line == b"Hello\r\n":
	print("Work")
print("OK")