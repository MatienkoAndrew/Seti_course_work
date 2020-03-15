#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from datetime import *
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
	speed_u = unicode(speed, 'utf-8')
	if speed_u.isnumeric() == False or int(speed) not in BAUDRATES:
		showerror("Bad baudrate.", speed + " не существует")
		return False
	byte_size = size_b.get()
	byte_size_u = unicode(byte_size, 'utf-8')
	if byte_size_u.isnumeric() == False or int(byte_size) not in BYTESIZES:
		showerror("Bad bytesize.", byte_size + " не существует")
		return False
	parity = parity_b.get()
	if parity not in PARITIES:
		showerror("Bad parity.", parity + " не существует")
		return False
	stopbits = bit_stop.get()
	stopbits_u = unicode(stopbits, 'utf-8')
	if stopbits_u.isnumeric() == False or int(stopbits) not in STOPBITS:
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
	global ser
	ser = Serial()
	window = configure_window()
	ser.port = port
	ser.baudrate = speed
	ser.bytesize = int(byte_size)
	ser.parity = parity
	ser.stopbits = int(stopbits)
	# ser.timeout = 2
	window_1 = chat(ser)
	# ser.open()
	print(ser)

def chat(ser):
	global out_flag
	global tr_in
	global in_list

	# -- массив полученных строк
	in_list = []
	# -- признаки занятости ввода-вывода
	out_flag = []


	def check_connect():
		time.sleep(10)
		while True:
			if ser.is_open:
				listbox.insert(END, datetime.strftime(datetime.now(), "%H:%M:%S") + " ACK_LINKACTIVE")
				# ser.write("ACK_LINKACTIVE\r\n".encode('utf-8'))
				ser.ft_write("ACK_LINKACTIVE")

				time.sleep(10)

	global in_st
	in_st = []
	# функция приема строки
	def fn_in():
		global in_list
		global in_st
		while 1:
			if ser.is_open:
				# --ждем прихода к нам строки
				while ser.in_waiting > 0:
					if ser.is_open:
						# window.after(10000, check_connect)
						# in_st = ser.readline()
						data_to_read = ser.in_waiting
						in_st = ser.ft_read(data_to_read)
						# if in_st == b"ACK_LINKACTIVE\r\n":
						if in_st == "ACK_LINKACTIVE":
							listbox.insert(END,  datetime.strftime(datetime.now(), "%H:%M:%S") + " LINKACTIVE")
							in_st = []
						else:
							# if in_st != b'':
							if in_st != '':
								in_list.append(in_st)
				time.sleep(1)   ##-- CPU не будет нагреваться до 100C
						# in_len = len(in_st)
				## -- ждем освобождения входного буфера и записываем в него
				# if ser.is_open:
				# 	if in_st != []:
				# 		in_list.append(in_st)
				# 	time.sleep(1)

	## -- запустить поток приема
	global start_thread
	start_thread = 0
	tr_in = threading.Thread(target=fn_in)
	tr_in.daemon = True
	# tr_in.start()

	thread_2 = threading.Thread(target=check_connect)
	thread_2.daemon = True

	## -- запустить основной поток
	def fn_out():
		global out_flag
		out_flag = 1

	##--Отправление сообщений(через кнопку "Отправить"
	global buffer_for_source_message
	buffer_for_source_message = []

	def fn_send():
		global user_name
		out_st = enter.get()
		if len(out_st) > 0:
			# ser.write((out_st + '\r\n').encode('utf-8'))
			ser.ft_write((out_st + '\r\n'))
			listbox.insert(END, user_name + ": " + out_st)
			buffer_for_source_message.append(user_name + ": " + out_st)
			try:
				listbox_source.insert(END, user_name + ": " + out_st)
			except:
				print("Source message window is closed")
		enter.delete(0, END)

	## == вывести строки в листбокс
	global buffer_for_dest_message
	buffer_for_dest_message = []

	def fn_disp():
		global out_flag
		while len(in_list) > 0:
			st = in_list.pop(0)
			listbox.insert(END, st)
			buffer_for_dest_message.append(st)
			try:
				listbox_dest.insert(END, st)
			except:
				print("Destination message window is closed")
		if out_flag:
			fn_send()
			out_flag = 0
		window.after(100, fn_disp)

	window = Tk()
	window.geometry('716x400')

	scrollbar = Scrollbar(window)
	scrollbar.pack(side=RIGHT, fill=Y)

	listbox = Listbox(window, yscrollcommand=scrollbar.set, font=('Calibri', 12))
	listbox.place(x=0, y=0, width=600, height=340)

	scrollbar.config(command=listbox.yview)

	enter = Entry(window, font=('Calibri', 15))
	enter.place(x=0, y=340, width=600, height=40)

	def open_port():
		global ser
		global tr_in
		global start_thread
		state = DISABLED
		if ser.is_open == False:
			ser.open()
			if ser.is_open:
				listbox.insert(END, "Port " + ser.port + " is opened")
				button_open.config(text="Закрыть порт")
				button_display.config(state=NORMAL)
				# if tr_in._started._flag == False:
				if start_thread == 0:
					tr_in.start()
					thread_2.start()
					start_thread = 1
		else:
			ser.close()
			if ser.is_open == False:
				listbox.insert(END, "Port " + ser.port + " is closed")
				button_open.config(text="Открыть порт")
				button_display.config(state=DISABLED)
	button_open = Button(window, text="Открыть порт", command=open_port) #command=open_port(ser))
	button_open.place(x=600,y=0, width=100, height=40)

	def about_program():
		global open_temp_window
		if len(mainmenu.master.children) == 7:
		# if '!toplevel' not in mainmenu.master.children.keys():
			temp_window = Toplevel(window)
			temp_window.title('О программе')
			temp_window.geometry('300x100')
			student_1 = Label(temp_window, text="Анастасия Молева", font=('Arial', 15))
			student_1.grid(row=0,column=0)
			student_2 = Label(temp_window, text="Матиенко Андрей", font=('Arial', 15))
			student_2.grid(row=1,column=0)
			student_3 = Label(temp_window, text="Белоусов Евгений", font=('Arial', 15))
			student_3.grid(row=2,column=0)
			open_temp_window = 1
				# mainmenu.entryconfig(1, state=DISABLED)
		# else:
		# 	mainmenu.entryconfig(1, state=DISABLED)
		# 	open_temp_window = 0

	mainmenu = Menu(window)
	window.config(menu=mainmenu)
	global open_temp_window
	open_temp_window = 0
	mainmenu.add_command(label="О программе", command=about_program)

	##--Исходящие сообщения(source_message)
	def source_message():
		global listbox_source
		window_source_message = Toplevel(window)
		window_source_message.title('Исходящие сообщения')
		window_source_message.geometry('600x400+500+200')
		listbox_source = Listbox(window_source_message, font=('Calibri', 12))
		listbox_source.place(x=0, y=0, width=600, height=340)
		for i in buffer_for_source_message:
			listbox_source.insert(END, i)

	button_source_message = Button(window, text='Исходящие', command=source_message)
	button_source_message.place(x=600,y=200, width=100,height=40)
	##----------------

	##--Приходящие сообщения(destination_message)
	def dest_message():
		global listbox_dest
		window_dest_message = Toplevel(window)
		window_dest_message.title('Приходящие сообщения')
		window_dest_message.geometry('600x400+800+200')
		listbox_dest = Listbox(window_dest_message, font=('Calibri', 12))
		listbox_dest.place(x=0, y=0, width=600, height=340)
		for i in buffer_for_dest_message:
			listbox_dest.insert(END, i)

	button_dest_message = Button(window, text='Приходящие', command=dest_message)
	button_dest_message.place(x=600,y=250,width=100,height=40)
	##---------------------

	button_display = Button(window, text='Отправить', command=fn_out, state=DISABLED)
	button_display.place(x=600, y=340, width=100, height=40)
	window.after(10, fn_disp)
	window.mainloop()

if __name__== "__main__":
	main()