import sqlite3 as sql
from pathlib import Path

def createDatabase(name):
    with open(f'{path}{name}.db', 'a') as f:
        pass

def createTable(db, name, cols, primaryKey):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        colList = ', '.join(cols)
        command = f'CREATE TABLE {name} ({colList})'
        cur.execute(command)
        con.commit()
        con.close() 
        print(command)
    except Exception as e:
        print(e)

def runCommand(db, comm):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        command = comm
        cur.execute(command)
        con.commit()
        con.close() 
        print(command)
    except Exception as e:
        print(e)

def insertUser(db, uname, passwd):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        command = f'INSERT INTO login VALUES(Null, "{uname}", "{passwd}")'
        cur.execute(command)
        con.commit()
        con.close() 
        print(command)
    except Exception as e:
        print(e) 

def insertExpression(db, uname, expr):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        command = f'INSERT INTO expressions VALUES(Null, "{uname}", "{expr}")'
        cur.execute(command)
        con.commit()
        con.close() 
        print(command)
    except Exception as e:
        print(e)   

path = f'{Path().resolve()}\\accounts\\'

# createTable('user_data', 
#             'login', 
#             [   'ID INTEGER PRIMARY KEY',
#                 'uname TEXT NOT NULL',
#                 'pass TEXT NOT NULL'
#             ],
#             None)

# createTable('user_data', 
#             'expressions', 
#             [   'ID INTEGER PRIMARY KEY',
#                 'uname TEXT NOT NULL',
#                 'expr TEXT NOT NULL'
#             ],
#             None)