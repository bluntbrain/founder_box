import sqlite3

connection = sqlite3.connect("svm_data.db")
crsr = connection.cursor()

sql_command = """INSERT INTO emp VALUES ("52b1661f","Ishan","1234","8200608175","602");"""
crsr.execute(sql_command)

sql_command = """INSERT INTO emp VALUES ("a77b3c27","Keval","1234","8200608175","811");"""
crsr.execute(sql_command)

connection.commit()
connection.close()