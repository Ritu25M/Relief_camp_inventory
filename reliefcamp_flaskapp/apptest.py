from flask import Flask,render_template,flash, redirect,url_for,session,logging,request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


app = Flask(__name__)

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


@app.route("/")
def index():
    return render_template("home.html")


@app.route('/Relief_Camps_List')
def relief_camps_list():
    return """<h1>Relief Camps!</h1>"""


@app.route("/Survivors_entry")
def survivor_entry():
    return render_template("login_register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        sheet = client.open("hlogininfo").sheet1
        c1 = sheet.find(uname)
        p1 = sheet.cell(c1.row, c1.col + 1).value
        if p1 == passw:
            return redirect(url_for("add_survivor"))
        else:
            """<h1>Invalid Credentials!</h1>"""
            redirect(url_for("login"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        sheet = client.open("hlogininfo").sheet1

        #sid = sheet.cell(1, 1).value
        insertuser = ["rand124", uname, mail, passw]
        sheet.insert_row(insertuser, 2)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/add_survivor", methods=["GET", "POST"])
def add_survivor():
    if request.method == "POST":
        gender = request.form['q71_gender']
        name = request.form.get('q95_name')
        ticketno = request.form.get('q91_aadharNumber')
        age = request.form.get('q93_age')
        day = request.form.get('q96_dateOf[day]')
        month = request.form.get('q96_dateOf[month]')
        year = request.form.get('q96_dateOf[year]')
        dateofentry = "-".join([day,month,year])
        sanitary = request.form.get('q81_isSanitary')
        corona = request.form.get('q76_areCorona')
        medical = request.form.get('q97_medicalRequirements')
        ocmnts = request.form.get('q17_includeOther17')

        sheet = client.open("survivors_info").sheet1

        #sid = sheet.cell(0, 1).value
        insertsurvivor = [dateofentry, ticketno, gender, name,age,"","yes","", sanitary, corona, "",medical, ocmnts]
        sheet.insert_row(insertsurvivor, 2)

        #pprint(gender)
        #print("Successfully added survivor!")
        return """<h1>Successfully added survivor!</h1>"""
    return render_template("test1.html")


if __name__ == "__main__":
    app.run(debug=True)