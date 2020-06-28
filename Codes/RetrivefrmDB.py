import sqlite3 as db


def getdetailsname(name):
    if name == None or name =="Unknown":
        return 0

    else:
        conn = db.connect('Database.db')
        cur = conn.cursor()

        cur.execute("SELECT empid from employee where name = (?)", (name,))
        data = cur.fetchall()
        return data[0][0]


def getdetailsid(id1):
    conn = db.connect('Database.db')
    cur = conn.cursor()

    cur.execute("SELECT name from employee where empid = (?)", (id1,))
    data = cur.fetchall()
    return data[0][0]


def getalldetails(stype,skey):
    conn = db.connect('Database.db')
    cur = conn.cursor()
    if stype == 'name':
        try:
            cur.execute("SELECT empid,age,gender,contact from employee where name = (?)",(skey,))
            data = cur.fetchone()
            name = skey
            empid = data[0]
            age = data[1]
            gender = data[2]
            contact = data[3]
            return True, empid, name, age, gender, contact
        except ValueError:
            return False, None, None, None, None, None
        except TypeError:
            return False, None,None,None,None,None
    elif stype == 'id':
        try:
            cur.execute("SELECT name,age,gender,contact from employee where empid = (?)",(skey,))
            data = cur.fetchone()
            name = data[0]
            empid = skey
            age = data[1]
            gender = data[2]
            contact = data[3]
            return True, empid,name,age,gender,contact
        except ValueError:
            return False, None,None,None,None,None
        except TypeError:
            return False, None,None,None,None,None
    elif stype == 'age':
        try:
            cur.execute("SELECT empid,name,gender,contact from employee where age = (?)",(skey,))
            data = cur.fetchone()
            name = data[1]
            empid = data[0]
            age = skey
            gender = data[2]
            contact = data[3]
            return True, empid,name,age,gender,contact
        except ValueError:
            return False, None,None,None,None,None
        except TypeError:
            return False, None,None,None,None,None
    elif stype == 'contact':
        try:
            cur.execute("SELECT empid,age,gender,name from employee where contact = (?)",(skey,))
            data = cur.fetchone()
            name = data[3]
            empid = data[0]
            age = data[1]
            gender = data[2]
            contact = skey
            return True, empid,name,age,gender,contact
        except ValueError:
            return False, None,None,None,None,None
        except TypeError:
            return False, None,None,None,None,None


def getattend(colname):
    conn = db.connect('Database.db')
    cur = conn.cursor()
    attend = {}
    sql = "SELECT date," + colname + " from TimeIN"
    cur.execute(sql)
    data = cur.fetchall()
    sql = "SELECT date," + colname + " from TimeOUT"
    cur.execute(sql)
    data1 = cur.fetchall()
    for i in data:
        attend[i[0]] = [i[1]]
    for i in data1:
        attend[i[0]].append(i[1])
    return attend


def getlist():
    name, empid, age, gender, contact = [], [], [], [], []
    conn = db.connect('Database.db')
    cur = conn.cursor()
    cur.execute("SELECT name,empid,age,gender,contact from employee")
    while True:
        try:
            data = cur.fetchone()
            if data == None:
                raise Exception("End of line error!")
            elif data[1] == 0:
                pass
            else:
                name.append(data[0])
                empid.append(str(data[1]))
                age.append(str(data[2]))
                gender.append(data[3])
                contact.append(str(data[4]))
        except Exception:
            break
    length = len(name)
    return length, name, empid, age, gender, contact
