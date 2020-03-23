# import serial
# import time
# from ft_serial_1 import *
#
# ser_1 = Serial('COM3')
# ser_2 = Serial('COM4')
# ser_1.ft_write("Hello world")
# data_to_read = ser_2.in_waiting
# if data_to_read > 0:
# 	line = ser_2.ft_read(data_to_read)
# 	if line == "Hello world":
# 		print("OK")
# 	print(line)
# ser_2.ft_write("Yeah, Hello\r\n")
# data_to_read = ser_1.in_waiting
# if data_to_read > 0:
# 	line = ser_1.ft_read(data_to_read)
# 	print(line)
from tkinter import *
from tkinter.ttk import *

window = Tk()

def about_program():
		# global open_temp_window
		# if open_temp_window == 0:
			temp_window = Toplevel(window)
			temp_window.title('О программе')
			temp_window.geometry('300x100')
			student_1 = Label(temp_window, text="Анастасия Молева", font=('Arial', 15))
			student_1.grid(row=0, column=0)
			student_2 = Label(temp_window, text="Матиенко Андрей", font=('Arial', 15))
			student_2.grid(row=1, column=0)
			student_3 = Label(temp_window, text="Белоусов Евгений", font=('Arial', 15))
			student_3.grid(row=2, column=0)
			open_temp_window = 1
			mainmenu.entryconfig(1, state=DISABLED)
		# else:
		# 	mainmenu.entryconfig(1, state=DISABLED)
			# open_temp_window = 0


mainmenu = Menu(window)
window.config(menu=mainmenu)
# global open_temp_window
# open_temp_window = 0
mainmenu.add_command(label="О программе", command=about_program)
temp_window = Toplevel(window)
if temp_window.state()=="normal":
	print("wokawdo")
temp_window = Toplevel(window)
if mainmenu.master.children['!toplevel']:
	print("OK")
temp_window.destroy()
if temp_window.state()=="normal":
	print("KAOWDKoaKWD")
else:
	print("aowdjaod")
# if len(mainmenu.master.children) == 1:
if '!toplevel' not in mainmenu.master.children:
	print("OK")
temp_window.title('О программе')
temp_window.geometry('300x100')
student_1 = Label(temp_window, text="Анастасия Молева", font=('Arial', 15))
student_1.grid(row=0, column=0)
student_2 = Label(temp_window, text="Матиенко Андрей", font=('Arial', 15))
student_2.grid(row=1, column=0)
student_3 = Label(temp_window, text="Белоусов Евгений", font=('Arial', 15))
student_3.grid(row=2, column=0)
# open_temp_window = 1
mainmenu.entryconfig(1, state=DISABLED)
window.mainloop()

