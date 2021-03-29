import sqlite3
conn = sqlite3.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE khach_hang (email TEXT, mskh TEXT,passwd TEXT)')
conn.execute('CREATE TABLE thanh_toan (mstt TEXT,email TEXT,mskh TEXT,money TEXT,Oauth TEXT,day_start NUMERIC,day_end NUMERIC)')
conn.close()
