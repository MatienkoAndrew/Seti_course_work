# coding: utf-8
import threading
import time
import serial
from tkinter import *

# -- массив полученных строк
in_list = []
# -- признаки занятости ввода-вывода
out_flag = []

ser = serial.Serial('COM3', 9600, timeout=1)

# функция приема строки
def fn_in():
	global in_list
	while 1:
		# --ждем прихода к нам строки
		in_len = 0
		while in_len < 1:
			in_st = ser.readline()
			in_len = len(in_st)
		## -- ждем освобождения входного буфера и записываем в него
		in_list.append(in_st)
		time.sleep(1)

## -- запустить поток приема
tr_in = threading.Thread(target=fn_in)
tr_in.daemon = True
tr_in.start()

## -- запустить основной поток
def fn_out():
	global out_flag
	out_flag = 1

def fn_send():
	out_st = ed.get()
	if len(out_st) > 0:
		ser.write(out_st.encode())
		lb.insert(END, ">>>" + out_st)
	ed.delete(0, END)

## == вывести строки в листбокс
def fn_disp():
	global out_flag
	while len(in_list) > 0:
		st = in_list.pop(0)
		lb.insert(END, st)
	if out_flag:
		fn_send()
		out_flag = 0
	root.after(100, fn_disp)

root = Tk()
lb = Listbox(root, width=20, height=5, font=('Calibri', 20))
lb.pack()
ed = Entry(root, width=20, font=('Calibri', 20))
ed.pack()
bt = Button(root, text="send", width=20, command=fn_out, font=('Calibri', 20))
bt.pack()
root.after(10, fn_disp)
root.mainloop()


#! /usr/bin/env python
# -*- coding: utf-8 -*-