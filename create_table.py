import sqlite3

connection = sqlite3.connect("svm_data.db")
crsr = connection.cursor()
sql_command = """CREATE TABLE emp (
uid VARCHAR(12),
name VARCHAR(20),
password VARCHAR(4),
phone_number VARCHAR(10),
balance VARCHAR(4));"""
crsr.execute(sql_command)

connection.commit()
connection.close()