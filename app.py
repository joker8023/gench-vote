import datetime
import multiprocessing
import sqlite3

import xlrd

from votelib import VoteHelper

data_result = {'200':0,'206':0,'211':0,'204':0}

#刷评论
def comment():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("""
SELECT id,
                 [username]
                 ,[password]
             FROM user 
        """)
    print(cursor.fetchall())
    # for r in cursor.fetchall():
    #     usernmae = r[0]
    #     password = r[1]
    #     helper = VoteHelper()
    #     result = helper.addcomment(usernmae, password)
    #     print(result)
#c多进程
def main():
    batch = 20
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("""
           SELECT id,
                 [username]
                 ,[password]
             FROM user where id >1200
               """)
    useralllist =  c.fetchall()
    useralllist = list(useralllist)
    print(len(useralllist))
    split = len(useralllist) / batch
    multiprocessing_list = []
    for i in range(batch):
        if i != (batch - 1):
            userlist = useralllist[int(split * i): int(split * (i + 1))]
        else:
            userlist = useralllist[int(split * i):]
        p = multiprocessing.Process(target=mulitvote, args=(userlist,))
        p.start()
        multiprocessing_list.append(p)
    for p in multiprocessing_list:
        p.join()

# 544629 赵永安
# 544631 张林森
# 544635 暴亦金
# 544637 杨洋
# 544627 杜芳泽
#投票
def mulitvote(userlist):
    for user in userlist:
        username = user[1]
        password = user[2]
        helper = VoteHelper()
        helper.vote(username,password,166525,24993,544629,544631,544635,544637,544627,5,6,7,8,9)

def checklogin():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("""
              SELECT id,
                    [username]
                    ,[password]
                FROM user 
                  """)
    list = []
    for user in  c.fetchall():
        helper = VoteHelper()
        if helper.logincheck(user[1],user[2]):
            if  user[1]  not in list:
                list.append(user[1])
                c.execute('''INSERT INTO users (id,username, password)  VALUES (?,?,?)''',[None,user[1],user[2]])
    conn.commit()
    conn.close()

#获取excel数据
def getuser():
    data = xlrd.open_workbook('1.xlsx')
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    for rownum in range(0, nrows):
        row = table.row_values(rownum)
        if row:
            ID = str(row[0]).replace('.0','')
            username = str(row[1]).replace('.0','')
            password = str(row[2]).replace('.0','')
        c.execute('''INSERT INTO user (ID,username, password)  VALUES (?,?,?)''',[ID,username,password])
    conn.commit()
    conn.close()


if __name__ == '__main__':
    starttime = datetime.datetime.now()
    main()
    endtime = datetime.datetime.now()
    print(starttime,endtime)
