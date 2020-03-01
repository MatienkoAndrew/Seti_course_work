#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
import serial
from serial.tools import list_ports
from tkinter import *
from tkinter.ttk import *
from ft_serial_1 import *
from tkinter.messagebox import *
BAUDRATES = (50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800,
             9600, 19200, 38400, 57600, 115200, 230400, 460800, 500000,
             576000, 921600, 1000000, 1152000, 1500000, 2000000, 2500000,
             3000000, 3500000, 4000000)
PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'None', 'Even', \
                                                                  'Odd', 'Mark', 'Space'
STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)

PARITY_NAMES = {
    PARITY_NONE: 'None',
    PARITY_EVEN: 'Even',
    PARITY_ODD: 'Odd',
    PARITY_MARK: 'Mark',
    PARITY_SPACE: 'Space',
}

FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
BYTESIZES = (FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS)
PARITIES = (PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE)
STOPBITS = (STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO)

##-- Настройки
user_name = []
port = []
speed = []
byte_size = []
parity = []
stopbits = []

def validation(name, com_port, speed_b, size_b, parity_b, bit_stop):
	global user_name
	global port
	global speed
	global byte_size
	global parity
	global stopbits

	user_name = name.get()
	if not user_name:
		showerror("Username isn't define.", "Пожалуйста, введите имя")
		return False
	port = com_port.get()
	if port not in cut_port:
		showerror("Bad COM-port.", port + " не существует")
		return False
	speed = speed_b.get()
	if speed.isnumeric() == False or int(speed) not in BAUDRATES:
		showerror("Bad baudrate.", speed + " не существует")
		return False
	byte_size = size_b.get()
	if byte_size.isnumeric() == False or int(byte_size) not in BYTESIZES:
		showerror("Bad bytesize.", byte_size + " не существует")
		return False
	parity = parity_b.get()
	if parity not in PARITIES:
		showerror("Bad parity.", parity + " не существует")
		return False
	stopbits = bit_stop.get()
	if stopbits.isnumeric() == False or int(stopbits) not in STOPBITS:
		showerror("Bad stopbit.", stopbits + " не существует")
		return False
	return True


cut_port = []
##---Обрезаем полное имя COM-порта
def cut_port_name(str):
	global cut_port
	for i in range(len(str)):
		cut_port.append(str[i])
		cut_port[i] = cut_port[i].device
	return cut_port

def configure_window():
	"""Создание окна настроек параметров"""
	conf_window = Tk()
	conf_window.geometry('500x300')
	conf_window.title('Настройки')

	"""Имя пользователя"""
	label_name = Label(conf_window, text='Имя пользователя:', font=("Calibri", 15))
	label_name.grid(row=0, column=0)
	name = Entry(conf_window, width=20)
	name.grid(row=0, column=1)

	"""COM-port"""
	label_port = Label(conf_window, text='Порт:', font=("Calibri", 15))
	label_port.grid(row=1, column=0)
	com_port = Combobox(conf_window)
	com_port['values'] = cut_port_name(list_ports.comports())
	com_port.current(0)
	com_port.grid(row=1, column=1)

	"""Скорость обмена"""
	label_speed = Label(conf_window, text='Скорость:', font=("Calibri", 15))
	label_speed.grid(row=2, column=0)
	speed_b = Combobox(conf_window)
	speed_b['values'] = BAUDRATES
	speed_b.current(12)
	speed_b.grid(row=2, column=1)

	"""Размер байта"""
	label_byte_size = Label(conf_window, text='Размер байта:', font=("Calibri", 15))
	label_byte_size.grid(row=3, column=0)
	size_b = Combobox(conf_window)
	size_b['values'] = BYTESIZES
	size_b.current(3)
	size_b.grid(row=3, column=1)

	"""Бит четности"""
	label_bit_parity = Label(conf_window, text='Бит четности:', font=("Calibri", 15))
	label_bit_parity.grid(row=4, column=0)
	parity_b = Combobox(conf_window)
	parity_b['values'] = PARITIES
	parity_b.current(0)
	parity_b.grid(row=4, column=1)

	"""Стоп бит"""
	label_stop_bit = Label(conf_window, text='Стоп бит:', font=("Calibri", 15))
	label_stop_bit.grid(row=5, column=0)
	bit_stop = Combobox(conf_window)
	bit_stop['values'] = STOPBITS
	bit_stop.current(0)
	bit_stop.grid(row=5, column=1)

	##-- Настройки сохраняются
	def clicked():
		if validation(name, com_port, speed_b, size_b, parity_b, bit_stop):
			conf_window.destroy()

	"""Кнопка завершения настроек"""
	button = Button(conf_window, text="OK", command=clicked)
	button.grid(column=2)
	conf_window.mainloop()


def main():
	ser = Serial()
	window = configure_window()
	ser.port = port
	ser.baudrate = speed
	ser.bytesize = int(byte_size)
	ser.parity = parity
	ser.stopbits = int(stopbits)
	ser.open()
	print(ser)

if __name__== "__main__":
	main()