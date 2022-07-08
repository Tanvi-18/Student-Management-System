from sqlite3 import *

con = connect("SMS.db")
cursor = con.cursor()
cursor.execute("CREATE TABLE student(rno INTEGER , name TEXT , marks INTEGER)")
con.commit()
		