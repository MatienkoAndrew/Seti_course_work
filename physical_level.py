#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
import serial
from tkinter import *
from ft_serial_1 import *

# # ser = serial.Serial('COM3')
# ser = Serial('COM3')
# print('Port1: ' + str(ser))
#
# # ser_1 = serial.Serial('COM4')
# ser_1 = Serial('COM4')
# print('Port2: ' + str(ser_1))
# ser.write(b'Hello\n')
# line = ser_1.readline(6)
# print(line)

in_list = []
out_flag = []

ser = Serial('COM3')

#----Get string
def fn_in():
	global in_list
	while True:
		in_len = 0
		while in_len < 1:
			in_st = ser.readline()
			in_len = len(in_st)
		in_list.append(in_st)
		time.sleep(1)

tr_in = threading.Thread(target=fn_in)
tr_in.daemon = True
tr_in.start()

def fn_out():
	global out_flag
	out_flag = 1

def fn_send():
	out_st = ed.get()
	if len(out_st) > 0:
		ser.write((out_st+ '\r\n').encode('utf-8'))
		lb.insert(END, ">>>" + out_st)
	ed.delete(0, END)

##-------Вывести строки в литсбокс
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
root.geometry("500x300")
lb = Listbox(root, width=20, height=5, font=('Arial', 20))
lb.pack()
ed = Entry(root, width=20, font=('Calibri', 20))
ed.pack()
bt = Button(root, text="send", width=20, command=fn_out, font=('Calibri', 20))
bt.pack()
root.after(10, fn_disp)
root.mainloop()
