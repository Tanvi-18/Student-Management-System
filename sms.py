# IMPORTS

from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import pandas as pd
import requests
import bs4

f_1 = ("Consolas", 11)
f_2 = ("Consolas", 16, 'bold')
f_3 = ("Consolas", 14)
main_bg = "#14000a"
main_fg = "#ffedd8"
button_bg = "#997b66"
button_fg = "#14000a"

# FUNCTIONS

def add_data():
	con = None
	try:
		if(not((add_window_ent_rno.get()).isdigit()) or add_window_ent_rno.get()== None):
			raise Exception("Roll number should not be empty or negative & should contain only integers")		
		if(not((add_window_ent_name.get()).isalpha()) or len(add_window_ent_name.get())< 2):
			raise Exception("Name should not be empty or numeric & should have minimum 2 characters")
		if(not((add_window_ent_marks.get()).isdigit()) or (not(0<= (int(add_window_ent_marks.get())) <=100))):
			raise Exception("Marks should not be empty and should be in range of 0 to 100")
		con = connect("SMS.db")
		print("Database created / open")
		cursor = con.cursor()
		sql = "insert into student values('%d', '%s', '%d')"
		rno = int(add_window_ent_rno.get())
		name = add_window_ent_name.get()
		marks = int(add_window_ent_marks.get())
		cursor.execute(sql % (rno, name, marks))
		con.commit()
		showinfo('Success', 'Record added')
	except Exception as e:
		showerror("Issue ", e)
		con.rollback()
	finally:
		add_window_ent_rno.delete(0, END)
		add_window_ent_name.delete(0, END)
		add_window_ent_marks.delete(0, END)
		if con is not None:
			con.close()
			

def view_data():
	view_window_st_data.delete(1.0, END)
	info = ""
	con = None
	try:
		con = connect("SMS.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + " Roll No :- " + str(d[0]) + " "  + "  Name :- " + str(d[1])  + " " + "  Marks :- "+ str(d[2]) +"\n"
		print(info)
		view_window_st_data.insert(INSERT, info)
	except Exception as e:
		showerror('Issue ', e)
	finally: 
		if con is not None:
			con.close()
	

def upd_data():
	try:
		con = None
		if(not((upd_window_ent_rno.get()).isdigit()) or upd_window_ent_rno.get()== None):
			raise Exception("Roll number should not be empty or negative & should contain only integers")		
		if(not((upd_window_ent_name.get()).isalpha()) or len(upd_window_ent_name.get())< 2):
			raise Exception("Name should not be empty or numeric & should have minimum 2 characters")
		if(not((upd_window_ent_marks.get()).isdigit()) or (not(0<= (int(upd_window_ent_marks.get())) <=100))):
			raise Exception("Marks should not be empty and should be in range of 0 to 100")
		con = connect("SMS.db")
		print("Database created / open")
		cursor = con.cursor()
		sql = "update student set name='%s', marks='%d' where rno='%d'"
		rno = int(upd_window_ent_rno.get())
		name = upd_window_ent_name.get()
		marks = int(upd_window_ent_marks.get())
		cursor.execute(sql % (name, marks, rno))
		print(cursor.rowcount)
		if cursor.rowcount > 0:
			showinfo('Sucess', 'Record updated')
			con.commit()
		else:
			print("Record does not exist ")
	except Exception as e:
		showerror("Issue ", e)
		con.rollback()
	finally:
		upd_window_ent_rno.delete(0, END)
		upd_window_ent_name.delete(0, END)
		upd_window_ent_marks.delete(0, END)
		if con is not None:
			con.close()
			

def del_data():
	try:
		con = None
		rno = int(del_window_ent_rno.get())
		con = connect("SMS.db")
		c = con.cursor()
		sql = "DELETE FROM student WHERE rno = %d"
		c.execute(sql % (rno))
		if (c.rowcount) > 0:
			showinfo("Success", f"Deleted data of Roll number {rno}")
			con.commit()
		else:
			showerror("Not found", f"Record with roll number {rno} does not exists")
	except Exception as e:
		showerror("Error", "Only Integer value is expected")
	finally:
		del_window_ent_rno.delete(0, END)
		if con is not None:
			con.close()

def chart():
	try:	
		marks = []
		name = []
		con = None
		con = connect("SMS.db")
		c = con.cursor()
		c.execute("SELECT name, marks from student")
		m = c.fetchall()
		for d in m:
			name.append(d[0])
			marks.append(d[1])
		plt.bar(name, marks, linewidth=4, color = ['#d0b8ac', "#d9ae94", '#baa587'])
		plt.xlabel("Names")
		plt.ylabel("Marks")
		plt.title("Batch Information")
		plt.show()
	except Exception as e:
		showerror("Failure", e)
	finally:
		if con is not None:
			con.close()

def location():
	try:
		wa = "https://ipinfo.io/"
		res = requests.get(wa)

		data = res.json()

		global city_name_l

		city_name_l = data['city']
		state_name_l = data['region']

		main_window_lbl_loc.config(text="  LOC: " + city_name_l + ", " + state_name_l)
		return
	except Exception as e:
		print("Error ocurred",e)
		main_window_lbl_loc.config(text="Location not found")


def temp():
	try:
		city_name_t = city_name_l

		a1 = "https://api.openweathermap.org/data/2.5/weather?units=metric"
		a2 = "&q=" + city_name_t
		a3 = "&appid=" + "e863f8eb4b575c9f7081d3befd43903d"
		wa = a1 + a2 + a3
		res = requests.get(wa)

		data = res.json()

		temp = data['main']['temp']
		main_window_lbl_temp.config(text="TEMPERATURE: "+ str(temp)+ "°C")
		return
	except Exception as e:
		print("Error ocurred",e)
		main_window_lbl_temp.config(text="Temperature not found")



def qotd():
	try:
		wa = "https://www.brainyquote.com/quote_of_the_day"
		res = requests.get(wa)
		data = bs4.BeautifulSoup(res.text, "html.parser")
		info = data.find('img', {'class':'p-qotd'})
		qotd1, qotd2 = info['alt'].split("-")
		main_window_lbl_qotd.config(text="QOTD: "+ qotd1 + "\n\t- " + qotd2)
	except Exception as e:
		print("Error:",e)
		main_window_lbl_qotd.config(text="QOTD not found")


def to_window_name(window_mf):
	window_mf.deiconify()
	main_window.withdraw()	

def to_main_window(window_name):
	main_window.deiconify()
	window_name.withdraw()

	
# MAIN WINDOW

main_window = Tk()
main_window.title("Student Management System")
main_window.geometry("620x500+400+100")
main_window.config(bg = main_bg)

main_window_btn_add = Button(main_window, text="ADD", width=18, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_window_name(add_window)])
main_window_btn_view = Button(main_window, text="VIEW", width=18, font=f_2,fg=button_fg, bg=button_bg, command=lambda:[to_window_name(view_window), view_data()])
main_window_btn_upd = Button(main_window, text="UPDATE", width=18, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_window_name(upd_window)])
main_window_btn_del = Button(main_window, text="DELETE", width=18, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_window_name(del_window)])
main_window_btn_charts = Button(main_window, text="CHARTS", width=18, font=f_2, fg=button_fg, bg=button_bg, command=chart)
main_window_lbl_loc = Label(main_window, text="Location:", width=25, height=8, wraplength=800, fg=main_fg, bg = main_bg, font=f_1)
main_window_lbl_temp = Label(main_window, text="Temperature:", width=25, height=8, wraplength=400, fg=main_fg, bg = main_bg, font=f_1)
main_window_lbl_qotd = Label(main_window, text="QOTD:", width=50, height=2, wraplength=950, fg=main_fg, bg = main_bg, font=f_1)


main_window_btn_add.grid(row = 1, column = 3, pady = 2)
main_window_btn_view.grid(row = 2, column = 3, pady = 2)
main_window_btn_upd.grid(row = 3, column = 3, pady = 2)
main_window_btn_del.grid(row = 4, column = 3, pady = 2)
main_window_btn_charts.grid(row = 5, column = 3, pady = 2)
main_window_lbl_loc.grid(row = 8, column = 2, pady = 3)
main_window_lbl_temp.grid(row = 8, column = 6, pady = 3)
main_window_lbl_qotd.grid(row = 12, column = 2, pady = 3, columnspan=7)

location()
temp()
qotd()


# ADD

add_window = Toplevel(main_window)
add_window.title("Add Student")
add_window.geometry("620x500+400+100")
add_window.config(bg = main_bg)

add_window_lbl_rno = Label(add_window, text="Enter Roll No.", width=15, fg=main_fg, bg = main_bg, font=f_3)
add_window_ent_rno = Entry(add_window, font=f_3)
add_window_lbl_name = Label(add_window, text="Enter Name", width=15, fg=main_fg, bg = main_bg, font=f_3)
add_window_ent_name = Entry(add_window, font=f_3)
add_window_lbl_marks = Label(add_window, text="Enter Marks", width=15, fg=main_fg, bg = main_bg, font=f_3)
add_window_ent_marks = Entry(add_window, font=f_3)
add_window_btn_save = Button(add_window, text="SAVE", width=15, font=f_2, fg=button_fg, bg=button_bg, command=add_data)
add_window_btn_back = Button(add_window, text="BACK", width=15, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_main_window(add_window)])

add_window_lbl_rno.pack(pady=5)
add_window_ent_rno.pack(pady=10)
add_window_lbl_name.pack(pady=2)
add_window_ent_name.pack(pady=10)
add_window_lbl_marks.pack(pady=2)
add_window_ent_marks.pack(pady=10)
add_window_btn_save.pack(pady=40)
add_window_btn_back.pack(pady=1)
add_window.withdraw()

# VIEW

view_window = Toplevel(main_window)
view_window.title("View Student")
view_window.geometry("620x500+400+100")
view_window.config(bg = main_bg)

view_window_st_data = ScrolledText(view_window, width=50, height=15, font=f_3)
view_window_btn_back = Button(view_window, text="BACK", width=15, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_main_window(view_window)])
view_window_st_data.pack(pady=10)
view_window_btn_back.pack(pady=30)
view_window.withdraw()


# UPDATE

upd_window = Toplevel(main_window)
upd_window.title("Update Student")
upd_window.geometry("620x500+400+100")
upd_window.config(bg = main_bg)

upd_window_lbl_rno = Label(upd_window, text="Enter Roll No.", width=15, fg=main_fg, bg = main_bg, font=f_3)
upd_window_ent_rno = Entry(upd_window, font=f_3)
upd_window_lbl_name = Label(upd_window, text="Enter Name", width=15,fg=main_fg, bg = main_bg, font=f_3)
upd_window_ent_name = Entry(upd_window, font=f_3)
upd_window_lbl_marks = Label(upd_window, text="Enter Marks", width=15, fg=main_fg, bg = main_bg, font=f_3)
upd_window_ent_marks = Entry(upd_window, font=f_3)
upd_window_btn_save = Button(upd_window, text="SAVE", width=15,font=f_2, fg=button_fg, bg=button_bg, command=upd_data)
upd_window_btn_back = Button(upd_window, text="BACK", width=15, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_main_window(upd_window)])

upd_window_lbl_rno.pack(pady=5)
upd_window_ent_rno.pack(pady=10)
upd_window_lbl_name.pack(pady=2)
upd_window_ent_name.pack(pady=10)
upd_window_lbl_marks.pack(pady=2)
upd_window_ent_marks.pack(pady=10)
upd_window_btn_save.pack(pady=40)
upd_window_btn_back.pack(pady=1)
upd_window.withdraw()


# DELETE

del_window = Toplevel(main_window)
del_window.title("Delete Student")
del_window.geometry("620x500+400+100")
del_window.config(bg = main_bg)

del_window_lbl_rno = Label(del_window, text="Enter Roll No.", width=15, fg=main_fg, bg = main_bg, font=f_3)
del_window_ent_rno = Entry(del_window, font=f_3)
del_window_btn_save = Button(del_window, text="SAVE", width=15, font=f_2, fg=button_fg, bg=button_bg, command=del_data)
del_window_btn_back = Button(del_window, text="BACK", width=15, font=f_2, fg=button_fg, bg=button_bg, command=lambda:[to_main_window(del_window)])

del_window_lbl_rno.pack(pady=10)
del_window_ent_rno.pack(pady=10)
del_window_btn_save.pack(pady=40)
del_window_btn_back.pack(pady=1)
del_window.withdraw()

main_window.mainloop()