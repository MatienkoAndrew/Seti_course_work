#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
from datetime import datetime
from tkinter import *

def chat(ser):
	global out_flag
	global tr_in
	global in_list

	# -- массив полученных строк
	in_list = []
	# -- признаки занятости ввода-вывода
	out_flag = []


	def give_username():
		while ser.another_username == None:
			time.sleep(1)
			if ser.is_open:
				ser.ft_write("Username" + str(ser.username))

	## counter - счетчик(строчка в listbox)
	## -- Отправленные сообщения таким образом становятся синими
	global counter
	counter = 0
	def check_connect():
		global counter
		time.sleep(10)
		while True:
			if ser.is_open:
				listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") +"] " + "ACK_LINKACTIVE")
				listbox.itemconfig(counter, {'fg': 'gray'})
				ser.ft_write("ACK_LINKACTIVE")
				counter += 1
				time.sleep(10)

	global in_st
	in_st = []
	# функция приема строки
	def fn_in():
		global counter
		global in_list
		global in_st
		while 1:
			if ser.is_open:
				# --ждем прихода к нам строки
				while ser.in_waiting > 0:
					if ser.is_open:
						data_to_read = ser.in_waiting
						in_st = ser.ft_read(data_to_read)
						if in_st == "ACK_LINKACTIVE":
							listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + " LINKACTIVE")
							listbox.itemconfig(counter, {'fg': 'gray'})
							counter += 1
							in_st = []
						elif in_st[:8] == "Username":
							ser.another_username = in_st[8:]
							in_st = []
						else:
							if in_st != '':
								in_list.append(in_st)
				time.sleep(1)   ##-- CPU не будет нагреваться до 100C

	## -- запустить поток приема
	global start_thread
	start_thread = 0
	tr_in = threading.Thread(target=fn_in)
	tr_in.daemon = True

	thread_2 = threading.Thread(target=check_connect)
	thread_2.daemon = True

	thread_3_name = threading.Thread(target=give_username)
	thread_3_name.daemon = True

	## -- запустить основной поток
	def fn_out():
		global out_flag
		out_flag = 1

	##--Отправление сообщений через кнопку "Отправить"
	global buffer_for_source_message
	buffer_for_source_message = []


	def fn_send():
		global counter
		# global user_name
		out_st = enter.get()
		if len(out_st) > 0:
			ser.ft_write((out_st + '\r\n'))
			listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ser.username + ": " + out_st)
			listbox.itemconfig(counter, {'fg': 'blue'})
			counter += 1
			buffer_for_source_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ser.username + ": " + out_st)
			try:
				listbox_source.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ser.username + ": " + out_st)
			except:
				print("Source message window is closed")
		enter.delete(0, END)

	## == вывести строки в листбокс
	global buffer_for_dest_message
	buffer_for_dest_message = []

	def fn_disp():
		global counter
		global out_flag
		while len(in_list) > 0:
			st = in_list.pop(0)
			if ser.another_username != None:
				listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ser.another_username + ": " + st)
				listbox.itemconfig(counter, {'fg': 'red'})
				counter += 1
				buffer_for_dest_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ser.another_username + ": " + st)
			else:
				listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ">>> " + st)
				listbox.itemconfig(counter, {'fg': 'red'})
				counter += 1
				buffer_for_dest_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S")+ "] " + ">>> " + st)
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
		global counter
		global tr_in
		global start_thread
		state = DISABLED
		if ser.is_open == False:
			ser.open()
			if ser.is_open:
				listbox.insert(END, "Port " + ser.port + " is opened")
				button_open.config(text="Закрыть порт")
				button_display.config(state=NORMAL)
				counter += 1
				if start_thread == 0:
					tr_in.start()
					thread_2.start()
					thread_3_name.start()
					start_thread = 1
		else:
			ser.close()
			if ser.is_open == False:
				listbox.insert(END, "Port " + ser.port + " is closed")
				button_open.config(text="Открыть порт")
				button_display.config(state=DISABLED)
				counter += 1
	button_open = Button(window, text="Открыть порт", command=open_port)
	button_open.focus_set()
	button_open.place(x=600,y=0, width=100, height=40)

	global counter_info_window
	counter_info_window = 0
	def about_program():
		"""Меню-справка о создателях программы
			Количество открытых окон не должно превышать одного"""
		global counter_info_window
		if counter_info_window == 0:
			temp_window = Toplevel(window)
			def close_window():
				global counter_info_window
				counter_info_window -= 1
				temp_window.destroy()
			temp_window.protocol("WM_DELETE_WINDOW", close_window)
			temp_window.title('О программе')
			temp_window.geometry('300x100')
			student_1 = Label(temp_window, text="Анастасия Молева", font=('Arial', 15))
			student_1.grid(row=0,column=0)
			student_2 = Label(temp_window, text="Матиенко Андрей", font=('Arial', 15))
			student_2.grid(row=1,column=0)
			student_3 = Label(temp_window, text="Белоусов Евгений", font=('Arial', 15))
			student_3.grid(row=2,column=0)
			counter_info_window += 1

	mainmenu = Menu(window)
	window.config(menu=mainmenu)
	mainmenu.add_command(label="О программе", command=about_program)

	##--Исходящие сообщения(source_message)
	global counter_source_window
	counter_source_window = 0
	def source_message():
		"""Окно - Отправленные сообщения
			Если окно открыто, то кнопка становится недоступной"""
		global listbox_source
		global counter_source_window
		if counter_source_window == 0:
			window_source_message = Toplevel(window)
			def close_window():
				global counter_source_window
				counter_source_window -= 1
				window_source_message.destroy()
				button_source_message.config(state='normal')
			window_source_message.protocol("WM_DELETE_WINDOW", close_window)
			window_source_message.title('Исходящие сообщения')
			window_source_message.geometry('600x400+500+200')
			listbox_source = Listbox(window_source_message, font=('Calibri', 12))
			listbox_source.place(x=0, y=0, width=600, height=340)
			counter_source_window += 1
			button_source_message.config(state=DISABLED)
			for i in buffer_for_source_message:
				listbox_source.insert(END, i)

	button_source_message = Button(window, text='Исходящие', command=source_message, state='normal')
	button_source_message.place(x=600,y=200, width=100,height=40)
	##----------------

	##--Приходящие сообщения(destination_message)
	global count_dest_window
	count_dest_window = 0
	def dest_message():
		"""Окно - Пришедшие сообщения
			Если окно открыто, то кнопка становится недоступной"""
		global listbox_dest
		global count_dest_window
		if count_dest_window == 0:
			window_dest_message = Toplevel(window)
			def close_window():
				global count_dest_window
				count_dest_window -= 1
				window_dest_message.destroy()
				button_dest_message.config(state='normal')
			window_dest_message.protocol("WM_DELETE_WINDOW", close_window)
			window_dest_message.title('Приходящие сообщения')
			window_dest_message.geometry('600x400+800+200')
			listbox_dest = Listbox(window_dest_message, font=('Calibri', 12))
			listbox_dest.place(x=0, y=0, width=600, height=340)
			button_dest_message.config(state=DISABLED)
			for i in buffer_for_dest_message:
				listbox_dest.insert(END, i)
			count_dest_window += 1

	button_dest_message = Button(window, text='Приходящие', command=dest_message, state='normal')
	button_dest_message.place(x=600,y=250,width=100,height=40)
	##---------------------

	button_display = Button(window, text='Отправить', command=fn_out, state=DISABLED,)
	button_display.place(x=600, y=340, width=100, height=40)
	window.after(10, fn_disp)
	window.mainloop()
