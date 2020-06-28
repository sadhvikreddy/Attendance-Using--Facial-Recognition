from flask import Flask, render_template, request, Response
from SourceCode.Web.Codes import getImage
from SourceCode.Web.Codes import InsertionIntoDB as idb
from SourceCode.Web.Codes.camera import VideoCamera
from SourceCode.Web.Codes import RetrivefrmDB as rdb
from SourceCode.Web.Codes import gt

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def homepage():
    return render_template('homepage.html')


# noinspection PyShadowingBuiltins
def gen(camera):
    while True:
        global pname
        frame, pname = camera.get_frame()
        # noinspection PyShadowingBuiltins
        id = rdb.getdetailsname(pname)
        colname = pname + str(id)
        idb.takeatten(colname)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gen1(camera):
    while True:
        global pname
        frame, pname = camera.get_frame()
        # noinspection PyShadowingBuiltins
        id = rdb.getdetailsname(pname)
        colname = pname + str(id)
        idb.takeatten1(colname)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/reg.html', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        global pdetails
        pdetails = []
        name = request.form.get('pname')
        age = request.form.get('age')
        gender = request.form.get('gender')
        contact = request.form.get('contact')
        pdetails.append(name)
        pdetails.append(age)
        pdetails.append(gender)
        pdetails.append(contact)
        x = '''<center><h2>Hello {}</h2>
               <h3>Face Scanning</h3></center>
               '''.format(name)
        x += render_template('reg1.html')
        return x
    else:
        return render_template('reg.html')


@app.route('/reg2.html', methods=['GET', 'POST'])
def reg2():
    getcam = getImage.capture()
    if request.method == 'POST':
        name = pdetails[0]
        age = pdetails[1]
        gender = pdetails[2]
        contact = pdetails[3]
        idb.insert(name, age, gender, contact)
        x = '''<script>alert("Sucess!, {}")
                window.location.href = "/"</script>'''.format(name)
        return x
    else:
        if getcam:
            name = pdetails[0]
            age = pdetails[1]
            gender = pdetails[2]
            contact = pdetails[3]
            x = ''' <center> <h2>Confirmation</h2><div class = "confirm">
                    <img src="static/InsertImage/file1.jpg" class="image">
                    <div class="middle"><div class="text">
                    <strong><u> Name</u> : </Strong>{}<br>
                    <strong><u> Age </u>: </Strong>{}<br>
                    <strong><u> Gender</u> : </Strong>{}<br>
                    <strong><u> Contact</u> : </Strong>{}<br></div></div></div>
                    </center>'''.format(name, age, gender, contact)
            x += render_template('reg2.html')
            return x
        else:
            x = '''<script>alert("No Faces Found!");
                           window.location.href = "reg.html"</script>'''
            x += render_template("reg.html")
            return x


@app.route('/display.html', methods=['POST', 'GET'])
def display():
    if request.method == 'POST':
        stype = request.form.get('searchtype')
        skey = request.form.get('searchkey')
        status, empid, name, age, gender, contact = rdb.getalldetails(stype, skey)
        if status:
            attenvalu = name + str(empid)
            attenda = rdb.getattend(attenvalu)
            x = render_template('display.html')
            x += '''<center><div class="card" align="center"><h2><br><br><center>Details</center></h2>'''
            x += '''<h3><center>empid = {}<br>
                    Name = {}<br>
                    Age = {}<br>
                    Gender = {}<br>
                    Contact = {}</center></h3></div>
                    '''.format(empid, name, age, gender, contact)
            x += '''<div class="card1"><h2><center>Attendance</center></h2>
                     <center>
                        <table width = "100%">
                            <tr>
                                <th>Date</th>
                                <th>Time In</th>
                                <th>Time Out</th>
                            </tr>'''
            table = ""
            for i in attenda:
                table = gt.gettable(table, i, attenda[i][0], attenda[i][1])
            table = gt.endtable(table)
            x = x + table
            return x
        else:
            x = render_template("display.html")
            return x + "<br><h3><center>Error Value Typed</center></h3><br>"
    else:
        return render_template('display.html')


@app.route('/CheckIN.html')
def CheckIN():
    return render_template('CheckIN.html')


@app.route('/facerecog')
def facerecog():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/CheckOut.html')
def CheckOut():
    return render_template('CheckOut.html')


@app.route('/facecheckout')
def facecheckout():
    return Response(gen1(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/dispall.html', methods=['POST', 'GET'])
def displayall():
    if request.method == "POST":
        empid1 = request.form.get("sk")
        length, name, empid, age, gender, contact = rdb.getlist()
        x = render_template("dispall.html")
        x += '''<br><br><center><div class="card3"><h2><center>Employees</center></h2>
                     <center>
                        <table width = "100%">
                            <tr>
                                <th>name</th>
                                <th>empid</th>
                                <th>age</th>
                                <th>gender</th>
                                <th>contact</th>
                            </tr>'''
        table = ""
        for i in range(length):
            table = gt.gettable1(table, name[i], empid[i], age[i], gender[i], contact[i])
        table = gt.endtable(table)
        x = x + table
        x += '''<center><br><br><h3>Enter Empid to show Attendance Details</h3>
                    <form method = "post">
                    <input type="text" placeholder="''' + empid1 + '''" name="sk" autofocus required autocomplete="off">
                        <input type = "submit">
                    </form>
                </center>'''
        name1 = rdb.getdetailsid(empid1)
        colname = name1 + str(empid1)
        attenda = rdb.getattend(colname)
        x += '''<br><center><div class="card2"><h2><center>Attendance</center></h2>
                             <center>
                                <table width = "100%">
                                    <tr>
                                        <th>Date</th>
                                        <th>Time In</th>
                                        <th>Time Out</th>
                                    </tr>'''
        table = ""
        for i in attenda:
            table = gt.gettable(table, i, attenda[i][0], attenda[i][1])
        table = gt.endtable(table)
        x = x + table
        return x
    else:
        length, name, empid, age, gender, contact = rdb.getlist()
        x = render_template("dispall.html")
        x += '''<center><br><br><div class="card2"><h2><center>Employees</center></h2>
                             <center>
                                <table width = "100%">
                                    <tr>
                                        <th>name</th>
                                        <th>empid</th>
                                        <th>age</th>
                                        <th>gender</th>
                                        <th>contact</th>
                                    </tr>'''
        table = ""
        for i in range(length):
            table = gt.gettable1(table, name[i], empid[i], age[i], gender[i], contact[i])
        table = gt.endtable(table)
        x = x + table
        x += '''<center><br><br><h3>Enter Empid to show Attendance Details</h3>
                    <form method = "post">
                    <input type="text" placeholder="Employee ID" name="sk" autofocus required autocomplete="off">
                        <input type = "submit">
                    </form>
                </center>'''
        return x


@app.route("/about.html")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(host='127.0.01', port=5000)
