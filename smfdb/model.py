import sqlite3
import sys
sys.path.append('..')

def getColumNames():
    con = sqlite3.connect('smfdb/smfDatabase.db')
    data = con.execute('select * from businessdataview limit 1')
    return [x[0] for x in data.description[2:]]
