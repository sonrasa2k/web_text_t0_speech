import sqlite3
conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE khach_hang (name TEXT, addr TEXT,sdt TEXT ,email TEXT, mskh TEXT,username TEXT, passwd TEXT)')
conn.execute('CREATE TABLE thanh_toan (mstt TEXT,username TEXT,mskh TEXT,money TEXT,Oauth TEXT,day_start NUMERIC,day_end NUMERIC)')
conn.close()
