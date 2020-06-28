import sqlite3 as db
import face_recognition as fr
import json
from datetime import datetime


def face():
    image1 = fr.load_image_file("file.jpg")
    img_encod = fr.face_encodings(image1)[0]

    a = img_encod.tolist()
    b = json.dumps(a)
    return b


def insert(name1,age1,gender1,contact1):
    conn = db.connect('Database.db')
    cur = conn.cursor()
    fd = face()
    cur.execute("INSERT into employee(name,age,gender,contact,facedata) VALUES (?,?,?,?,?)",(name1,age1,gender1,contact1,fd))
    cur.execute("SELECT empid from employee where name =(?)",(name1,))
    data = cur.fetchall()
    name = name1 + str(data[0][0])
    sql = "ALTER TABLE TimeIN add column " + name + " text"
    cur.execute(sql)

    sql = "ALTER TABLE TimeOUT add column " + name + " text"
    cur.execute(sql)
    conn.commit()


def takeatten(colname):
    conn = db.connect('Database.db')
    cur = conn.cursor()
    time = str(datetime.now().strftime('%HH:%MM'))
    date = str(datetime.now().strftime('%d-%m-%y'))
    try:
        sql = "INSERT INTO TimeIN (date," + colname + ") VALUES('" + date + "','" + time + "')"
        cur.execute(sql)
        sql1 = "INSERT INTO TimeOUT (date," + colname + ") VALUES('" + date + "','null')"
        cur.execute(sql1)
        t1 = cur.rowcount
        if t1 == 1:
            conn.commit()
    except db.IntegrityError:
        sql = "SELECT " + colname + " from TimeIN WHERE date=('" + date + "')"
        cur.execute(sql)
        data = cur.fetchall()
        if data[0][0] is None:
            sqlq = "UPDATE TimeIN set " + colname + "='" + time + "' WHERE date='" + date + "'"
            cur.execute(sqlq)
            sqlq1 = "UPDATE TimeOUT set " + colname + "='null' WHERE date='" + date + "'"
            cur.execute(sqlq1)
            t1 = cur.rowcount
            if t1 == 1:
                conn.commit()
    conn.close()


def takeatten1(colname):
    conn = db.connect('Database.db')
    cur = conn.cursor()
    time = str(datetime.now().strftime('%HH:%MM'))
    date = str(datetime.now().strftime('%d-%m-%y'))
    try:
        sql = "INSERT INTO TimeOUT (date," + colname + ") VALUES('" + date + "','" + time + "')"
        cur.execute(sql)
        t1 = cur.rowcount
        if t1 == 1:
            conn.commit()
    except db.IntegrityError:
        sql = "UPDATE TimeOUT set " + colname + "='" + time + "' WHERE date='" + date + "'"
        cur.execute(sql)
        t1 = cur.rowcount
        if t1 == 1:
            conn.commit()
    conn.close()
