# -*- coding: utf-8 -*-
import sqlite3
import os.path
import os
import json
from libs.version import compareVersions
AppData = None
NAME = 'sqlCoder'


def isPluginCorrect(path):
    if os.path.isdir(path):
        return True


def init(data):
    global AppData
    AppData = data


def initTable(dbPath: str = 'data/pluginsInfoDB.db') -> None:
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        # Init sqlite table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS plugins (
            name TEXT,
            version TEXT,
            status TEXT
        )
        """)
        con.commit()


def remove(name: str, dbPath: str = 'data/pluginsInfoDB.db') -> None:
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM plugins WHERE name=:name", {"name": name})
        # Close
        con.commit()


def insert(name: str, version: str, status: str, dbPath: str = 'data/pluginsInfoDB.db') -> None:
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO plugins VALUES (:name, :version, :status)", {
                    "name": name, "version": version, "status": status})
        con.commit()


def getPluginsList(dbPath: str = 'data/pluginsInfoDB.db') -> list:
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM plugins")
        response = cur.fetchall()
        con.commit()
        return response


def getVersion(name: str, dbPath: str = 'data/pluginsInfoDB.db') -> str:
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        cur.execute('SELECT (version) FROM plugins WHERE name=:name',
                    {"name": name})
        response = cur.fetchall()
        if response != []:
            response = response[0][0]
        return response


def getStatus(name: str, dbPath: str = 'data/pluginsInfoDB.db') -> str:
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        cur.execute('SELECT (status) FROM plugins WHERE name=:name',
                    {"name": name})
        response = cur.fetchall()
        if response != []:
            response = response[0][0]
        return response


def updateDB(dbPath: str = 'data/pluginsInfoDB.db') -> None:
    global isPluginCorrect
    # Connect
    with sqlite3.connect(dbPath) as con:
        cur = con.cursor()
        # Drop table
        cur.execute("DROP TABLE plugins")
        # Reinit it
        cur.execute("""
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
                cur.execute(
                    "INSERT INTO plugins VALUES (:name, :version, :status)", d)
        con.commit()
