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

	##-- Разрешение на запуск команд проверки соединения
	global permission_check_connect
	permission_check_connect = 0

	# -- массив полученных строк
	in_list = []
	# -- признаки занятости ввода-вывода
	out_flag = []


	global result_available
	result_available = threading.Event()

	def give_username():
		while ser.another_username == None:
			time.sleep(2)
			if ser.is_open:
				# result_available.wait(timeout=3)
				# ser.ft_write("Username" + str(ser.username))

				ser.ft_write_system("Username" + str(ser.username))
		pass





	##-- Буффер для команд
	global buffer_for_comand_message
	buffer_for_comand_message = []
	## counter - счетчик(строчка в listbox)
	## -- Отправленные сообщения таким образом становятся синими
	global counter
	counter = 0
	def check_connect():
		global counter
		while True:
			time.sleep(10)
			if ser.is_open and permission_check_connect:
				try:
					listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") +"] " + "LINKACTIVE")
				except:
					pass
				buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") +"] " + "LINKACTIVE")
				# ser.ft_write("LINKACTIVE")
				ser.ft_write_system("LINKACTIVE")



	global open_button_clicked
	##-- UPLINK-кадр
	##-- Кадр-запрос на разрешение соединения
	def try_connect():

		global result_available

		global counter
		global open_button_clicked
		open_button_clicked = 1
		while True:
			time.sleep(1)
			if ser.is_open and open_button_clicked:
				listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") +"] " + "Запрос на соединение")
				# listbox.itemconfig(counter, {'fg': 'gray'})
				counter += 1
				try:
					listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + "UPLINK")
				except:
					pass
				buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + "UPLINK")
				# ser.ft_write("UPLINK")
				ser.ft_write_system("UPLINK")

				# result_available.set()

				open_button_clicked = 0
			# time.sleep(1)
		pass


	##-- Функция:
	##-- Если через 10 секунд после передачи UPLINK не пришел ответ
	##-- то выводится сообщение о невозможности соединения
	global ACK_UPLINK_NOTCOME
	ACK_UPLINK_NOTCOME = 1
	def bad_connect():
		global counter
		counter_1 = 0
		while True:
			if ser.is_open:
				time.sleep(10)
				if ACK_UPLINK_NOTCOME == 1 and counter_1 == 0:
					listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + 'Соединение не установлено')
					counter_1 += 1
					counter += 1
			else:
				counter_1 = 0
			time.sleep(1)
		pass

	global push_close

	push_close = 0
	##-- DOWNLINK-кадр
	def downlink():
		global counter
		global push_close
		# while True:
		# 	time.sleep(1)
		# 	if push_close:
		listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + 'Разъединение')
		counter += 1
		try:
			listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + "DOWNLINK")
					# time.sleep(1)
					# listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + ">>> ACK_DOWNLINK")
		except:
			pass
		buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + "DOWNLINK")
				# time.sleep(1)
				# buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + ">>> ACK_DOWNLINK")
		push_close = 0
		# ser.ft_write("DOWNLINK")
		ser.ft_write_system("DOWNLINK")

	global linkactive_sent
	linkactive_sent = 1
	##-- Когда соединение разорвалось
	def bad_check_connect():
		global counter
		while True:
			time.sleep(13)
			if ser.is_open:#and permission_check_connect:
				if linkactive_sent == 0:
					listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "] " + 'Соединение разорвалось')
					counter += 1

	global in_st
	in_st = []
	# функция приема строки
	def fn_in():
		global counter
		global in_list
		global in_st

		global permission_check_connect
		global ACK_UPLINK_NOTCOME
		global linkactive_sent

		counter_temp = 0
		while 1:
			if ser.is_open:
				# --ждем прихода к нам строки
				while ser.in_waiting > 0:
					if ser.is_open:

						linkactive_sent = 0

						data_to_read = ser.in_waiting
						in_st = ser.ft_read(data_to_read)
						if in_st == "LINKACTIVE":
							try:
								listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> ACK_LINKACTIVE")
							except:
								pass
							buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> ACK_LINKACTIVE")

							linkactive_sent = 1

							in_st = []
						elif in_st[:8] == "Username":
							ser.another_username = in_st[8:]
							in_st = []
						elif in_st == "UPLINK":
							listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> Соединение установлено")
							counter += 1
							permission_check_connect = 1
							ACK_UPLINK_NOTCOME = 0
							try:
								listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> ACK_UPLINK")
							except:
								pass
							buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> ACK_UPLINK")
							in_st = []
						elif in_st == "DOWNLINK":
							listbox.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> Разъединение")
							counter += 1
							try:
								listbox_command.insert(END, "[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> ACK_DOWNLINK")
							except:
								pass
							buffer_for_comand_message.append("[" + datetime.strftime(datetime.now(), "%H:%M:%S") + "]" + ">>> ACK_DOWNLINK")
						else:
							if in_st != '':
								in_list.append(in_st)
				time.sleep(1)   ##-- CPU не будет нагреваться до 100C

	## -- запустить поток приема
	global start_thread
	start_thread = 0
	tr_in = threading.Thread(target=fn_in)
	tr_in.daemon = True

	thread_2_check_connect = threading.Thread(target=check_connect)
	thread_2_check_connect.daemon = True

	thread_3_name = threading.Thread(target=give_username)
	thread_3_name.daemon = True

	thread_4_try_connect = threading.Thread(target=try_connect)
	thread_4_try_connect.daemon = True

	thread_5_bad_connect = threading.Thread(target=bad_connect)
	thread_5_bad_connect.daemon = True

	thread_6_downlink = threading.Thread(target=downlink)
	thread_6_downlink.daemon = True

	thread_7_bad_check_connect = threading.Thread(target=bad_check_connect)
	thread_7_bad_check_connect.daemon = True

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
				pass
		enter.delete(0, END)

	## == вывести строки в листбокс
	global buffer_for_dest_message
	buffer_for_dest_message = []


	def fn_disp():
		global counter
		global out_flag

		while len(in_list) > 0:
			st = in_list.pop(0)


			st_1 = st.split('\n')
			st_1 = [message for message in st_1 if message]
			st_1 = [message + '\r\n' for message in st_1]

			for st in st_1:
				if "UPLINK" or "LINKACTIVE" in st:
					if "UPLINK" in st: st = st.replace("UPLINK", "")
					elif "LINKACTIVE" in st: st = st.replace("LINKACTIVE", "")

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
					pass
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

		global push_close
		global open_button_clicked

		if ser.is_open == False:
			ser.open()

			open_button_clicked = 1
			if ser.is_open:
				listbox.insert(END, "Port " + ser.port + " is opened")
				button_open.config(text="Закрыть порт")
				button_display.config(state=NORMAL)
				counter += 1
				if start_thread == 0:
					tr_in.start()
					thread_2_check_connect.start()
					thread_3_name.start()
					thread_4_try_connect.start()
					thread_5_bad_connect.start()
					# thread_6_downlink.start()
					# thread_7_bad_check_connect.start()
					start_thread = 1
		else:
			downlink()
			ser.close()
			if ser.is_open == False:
				listbox.insert(END, "Port " + ser.port + " is closed")
				button_open.config(text="Открыть порт")
				button_display.config(state=DISABLED)
				counter += 1
				push_close = 1

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
			window_dest_message.title('Входящие сообщения')
			window_dest_message.geometry('600x400+800+200')
			listbox_dest = Listbox(window_dest_message, font=('Calibri', 12))
			listbox_dest.place(x=0, y=0, width=600, height=340)
			button_dest_message.config(state=DISABLED)
			for i in buffer_for_dest_message:
				listbox_dest.insert(END, i)
			count_dest_window += 1

	button_dest_message = Button(window, text='Входящие', command=dest_message, state='normal')
	button_dest_message.place(x=600,y=250,width=100,height=40)


	##-- Окно команд(LINKACTIVE...)

	global count_command_window
	count_command_window = 0

	def command_button():
		"""Окно - сообщения команд
			Если окно открыто, то кнопка становится недоступной"""
		global listbox_command
		global count_command_window
		if count_command_window == 0:
			window_command_message = Toplevel(window)

			def close_window():
				global count_command_window
				count_command_window -= 1
				window_command_message.destroy()
				button_command_message.config(state='normal')

			window_command_message.protocol("WM_DELETE_WINDOW", close_window)
			window_command_message.title('Команды')
			window_command_message.geometry('600x400+800+200')
			listbox_command = Listbox(window_command_message, font=('Calibri', 12))
			listbox_command.place(x=0, y=0, width=600, height=340)
			button_command_message.config(state=DISABLED)
			for i in buffer_for_comand_message:
				listbox_command.insert(END, i)
			count_command_window += 1


	button_command_message = Button(window, text='Команды', command=command_button, state='normal')
	button_command_message.place(x=600, y=150, width=100, height=40)
	##---------------------

	button_display = Button(window, text='Отправить', command=fn_out, state=DISABLED,)
	button_display.place(x=600, y=340, width=100, height=40)
	window.after(10, fn_disp)
	window.mainloop()
