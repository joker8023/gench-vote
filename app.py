import datetime
import json
import pyodbc
import socket

import sqlite3

from votelib import VoteHelper


def connect_mssql1(host, db_name, user_name, password, autocommit=True, unicode_results=True):
    conn_string = "Driver={ODBC Driver 13 for SQL Server};Server=%s;Database=%s;UID=%s;PWD=%s"
    conn_string %= (host, db_name, user_name, password)
    conn = pyodbc.connect(conn_string, autocommit=autocommit, unicode_results=unicode_results)
    return conn

data_result = {'200':0,'206':0,'211':0,'204':0}

#刷评论
def comment():
    cursor = connect_mssql1('WONALIDBSTAGE', 'MSCNCMS', 'stagemscn', 'Dai2017!').cursor()
    cursor.execute("""
    SELECT
          [username]
          ,[password]
      FROM [MSCNCMS].[dbo].[userlist] order by id
        """)
    for r in cursor.fetchall():
        usernmae = r[0]
        password = r[1]
        helper = VoteHelper()
        result = helper.addcomment(usernmae, password)
        print(result)

def chuanjianbiao():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("""
      SELECT id,
            [username]
            ,[password]
        FROM user
          """)
    for r in c.fetchall():
        id = str(r[0])
        usernmae = r[1]
        password = r[2]
        print(id,usernmae,password)

if __name__ == '__main__':
    chuanjianbiao()