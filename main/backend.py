"""
Writer to sqlite3 database
"""
import sqlite3
import os

# Creates database if it does not exist, and sets up table:
def connect():
    if (os.path.isdir('outputs') != True):
        os.mkdir('outputs')
    conn=sqlite3.connect("outputs/Database_Measurements.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS measurement(id INTEGER PRIMARY KEY, date TEXT, time TEXT , localID INTEGER, measurement TEXT, secondsFromReference TEXT, printerNumber TEXT, designName TEXT, printParameters TEXT)")
    conn.commit()
    conn.close()

# Inserts a new entry into database:
def insert(Date, Time, localID, measurement, secondsFromReference, printerNumber, designName, printParameters):
    conn=sqlite3.connect("outputs/Database_Measurements.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO measurement VALUES (NULL,?,?,?,?,?,?,?,?)",(Date, Time, localID, measurement, secondsFromReference, printerNumber, designName, printParameters))
    print('localID: %d, New Measurement: %s' % (localID, measurement))
    print("Printer number: %s, Design name: %s, Print Parameters: %s" %(printerNumber, designName, printParameters))
    conn.commit()
    conn.close()

# Deletes the latest entry to the database (only applicable for push button triggering):    
def delete():
    conn=sqlite3.connect("outputs/Database_Measurements.db")
    cur=conn.cursor()
    cur.execute("DELETE FROM measurement WHERE id = (SELECT MAX(id) FROM measurement)")
    conn.commit()
    conn.close()

connect()
