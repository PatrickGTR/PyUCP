from flask import Flask,render_template,request,session,url_for,redirect,flash
import pymysql
import hashlib

from modules import app, connect_sql

@app.route("/", methods=["GET", "POST"])
def index():
    
    if session.get('remember_me'):
        session['logged_in'] = True
        username = session['username']
        return render_template("index.html", admins=retrieveAdmins())

    if request.method != "POST":
        return render_template("index.html", admins=retrieveAdmins())

    username = request.form.get('username')
    password = request.form.get('password')

    with connect_sql.MySQL() as c:
        c.execute("SELECT accountID, password, hash FROM accounts WHERE username=%s", username)
        results = c.fetchone()


    if not results:
        flash("Invalid password or username, please try again.", "danger")
        return render_template("index.html", admins=retrieveAdmins())

    retPassword, retSalt = results['password'], results['hash']
    password = hashlib.sha256(password.encode() + retSalt.encode()).hexdigest()

    if password.upper() != retPassword:
        flash("Wrong password, please try again.", "danger")
        return render_template("index.html", admins=retrieveAdmins())

    if request.form.get("checkbox"):
        session["remember_me"] = True
    
    session['logged_in'] = True
    session['username'] = results['accountID']
    flash("Successfully logged in", "success")
    
    return redirect(url_for('index'))

@app.route('/dashboard/<int:accountid>', methods=["GET", "POST"])
def dashboard(accountid):
    with connect_sql.MySQL() as c:
        c.execute(f"SELECT accountID, username, money, kills, deaths, jobID, score, experience, wantedlevel,  \
            DATE_FORMAT(registerdate, '%d %M %Y') as reg_date, \
            DATE_FORMAT(lastlogin, '%d, %M, %Y at %r') as last_log \
        FROM \
            accounts \
        WHERE \
            accountID={accountid}")
        results = c.fetchone()


    jobID = results['jobID']

    jobs = {
        0: "Drug Dealer",
        1: "Weapon Dealer",
        2: "Hitman",
        3: "Terrorist",
        4: "Rapist",
        5: "Mechanic"
    }
    jobName = jobs.get(jobID)
    
    return render_template("dashboard.html", results=results, jobName=jobName, admins=retrieveAdmins())

@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully logged out", "success")
    return redirect(url_for('index'))

def retrieveNameFromID(accountid):
    with connect_sql.MySQL() as c: 
        c.execute(f"SELECT username FROM accounts WHERE accountid={accountid}")
        result = c.fetchone()
    return result['username']

def retrieveAdmins():
    with connect_sql.MySQL() as c:
        c.execute("SELECT userID, adminLevel FROM admins")
        results = c.fetchall()
        print(results)
    return results

app.jinja_env.globals.update(retrieveNameFromID=retrieveNameFromID)