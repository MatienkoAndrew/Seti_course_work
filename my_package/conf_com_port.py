#! /usr/bin/env python
# -*- coding: utf-8 -*-
from tkinter import *
from tkinter.ttk import *
from my_package.configurations import BAUDRATES, BYTESIZES, PARITIES, STOPBITS
import serial
from serial.tools import list_ports
from my_package.validation import validation, cut_port_name

def configure_window(ser):
	global ok_button
	ok_button = False

	"""Создание окна настроек параметров"""
	conf_window = Tk()
	conf_window.geometry('500x300')
	conf_window.title('Настройки')

	"""Имя пользователя"""
	label_name = Label(conf_window, text='Имя пользователя:', font=("Calibri", 15))
	label_name.grid(row=0, column=0)
	default_name = StringVar(conf_window, value='Andrew')
	name = Entry(conf_window, width=20, textvariable=default_name)
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
	def clicked(event):
		global ok_button
		if validation(name, com_port, speed_b, size_b, parity_b, bit_stop, ser):
			conf_window.destroy()
			ok_button = True


	"""Кнопка завершения настроек"""
	button = Button(conf_window, text="OK", command=clicked)
	button.focus_set()
	button.bind('<Button-1>', clicked)
	button.bind('<Return>', clicked)
	button.grid(column=2)
	conf_window.mainloop()
	return ok_button