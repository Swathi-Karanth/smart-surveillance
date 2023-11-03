# Install Mysql on your computer
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python 

import mysql.connector

from website.models import EMERGENCY_CONTACTS

dataBase = mysql.connector.connect(
	host = 'localhost:3306',
	user = 'root',
	# passwd = 'Haechan@2023'
	passwd = 'mySQL_admin0'

	)

# 
cursorObject = dataBase.cursor() 

# Create a database
# cursorObject.execute("CREATE DATABASE campus_surveillance")
# cursorObject.execute(f"SELECT * FROM {EMERGENCY_CONTACTS}")
# results = cursorObject.fetchall()
# print(results)
