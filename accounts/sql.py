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
    except Exception as e:
        if debug:
            print(e)

def runCommand(db, comm):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        command = comm
        cur.execute(command)
        ret = cur.fetchall()
        con.commit()
        con.close() 
        return ret
    except Exception as e:
        if debug:
            print(e)

def insertUser(db, uname, passwd):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        command = f'INSERT INTO login VALUES(Null, "{uname}", "{passwd}")'
        cur.execute(command)
        con.commit()
        con.close() 
    except Exception as e:
        if debug:
            print(e) 

def insertExpression(db, uname, expr):
    try:
        con = sql.connect(f'{path}{db}.db')
        cur = con.cursor()
        command = f'INSERT INTO expressions VALUES(Null, "{uname}", "{expr}")'
        cur.execute(command)
        con.commit()
        con.close() 
    except Exception as e:
        if debug:
            print(e)   

path = f'{Path().resolve()}\\accounts\\'
debug = False

try:
    createDatabase('user_data')
    createTable('user_data', 
                'login', 
                [   'ID INTEGER PRIMARY KEY',
                    'uname TEXT NOT NULL',
                    'pass TEXT NOT NULL'
                ],
                None)

    createTable('user_data', 
                'expressions', 
                [   'ID INTEGER PRIMARY KEY',
                    'uname TEXT NOT NULL',
                    'expr TEXT NOT NULL'
                ],
                None)
except:
    pass