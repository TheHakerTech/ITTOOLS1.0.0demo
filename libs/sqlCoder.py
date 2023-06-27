# -*- coding: utf-8 -*-
import sqlite3
import os.path
import os
import json
from libs.version import compareVersions
AppData = None
isPluginCorrect = lambda path: os.path.exists(path+'/info.json') and os.path.exists(path+'/plugin.py')
def init(data):
    global AppData
    AppData = data

def initTable(dbPath: str = 'data/pluginsInfoDB.db') -> None:
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    # Init sqlite table
    cur.execute(r"DROP TABLE plugins")
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS plugins (
        name TEXT,
        version TEXT,
        status TEXT
    )
    """)
    con.commit()
    # Close
    cur.close()
    con.close()

def remove(name: str, dbPath: str = 'data/pluginsInfoDB.db') -> None:
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute(r"DELETE FROM plugins WHERE name=:name", {"name":name})
    # Close
    con.commit()
    cur.close()
    con.close()

def insert(name: str, version: str, status: str, dbPath: str = 'data/pluginsInfoDB.db') -> None:
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute(r"INSERT INTO plugins VALUES (:name, :version, :status)", {"name":name, "version":version, "status":status})
    con.commit()
    # Close
    cur.close()
    con.close()

def getPluginsList(dbPath: str = 'data/pluginsInfoDB.db') -> list:
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute(r"SELECT * FROM plugins")
    response = cur.fetchall()
    # Close
    con.commit()
    cur.close()
    con.close()
    return response

def getVersion(name: str, dbPath: str = 'data/pluginsInfoDB.db') -> str:
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute(r'SELECT (version) FROM plugins WHERE name=:name', {"name":name})
    response = cur.fetchall()
    if response != []:
        response = response[0][0]
    # Close
    cur.close()
    con.close()
    return response

def getStatus(name: str, dbPath: str = 'data/pluginsInfoDB.db') -> str:
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    cur.execute(r'SELECT (status) FROM plugins WHERE name=:name', {"name":name})
    response = cur.fetchall()
    if response != []:
        response = response[0][0]
    # Close
    cur.close()
    con.close()
    return response

def updateDB(dbPath: str = 'data/pluginsInfoDB.db') -> None:
    global isPluginCorrect
    # Connect
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    # Drop table
    cur.execute(r"DROP TABLE plugins")
    # Reinit it
    cur.execute(r"""
    CREATE TABLE IF NOT EXISTS plugins (
        name TEXT,
        version TEXT,
        status TEXT
    )
    """)
    folders = os.listdir('plugins/')
    for folderName in folders:
        folderPath = 'plugins/'+folderName
        if isPluginCorrect(folderPath):
            d = json.loads(open(folderPath+'/info.json').read())
            cur.execute(r"INSERT INTO plugins VALUES (:name, :version, :status)", d)
    con.commit()
    cur.close()
    con.close()