from flask import Flask,render_template,request,session,url_for,redirect,flash
import pymysql
import hashlib

from modules import app, connect_sql

@app.route("/", methods=["GET", "POST"])
def index():
    
    if session.get('remember_me'):
        session['logged_in'] = True
        username = session['username']
        return render_template("index.html")

    if request.method != "POST":
        return render_template("index.html")

    username = request.form.get('username')
    password = request.form.get('password')

    with connect_sql.sqlcursor() as c:
        c.execute("SELECT password, hash FROM accounts WHERE username=%s", username)
        results = c.fetchone()


    if not results:
        flash("Invalid password or username, please try again.", "danger")
        return render_template("index.html")

    retPassword, retSalt = results['password'], results['hash']
    password = hashlib.sha256(password.encode() + retSalt.encode()).hexdigest()

    if password.upper() != retPassword:
        flash("Wrong password, please try again.", "danger")
        return render_template("index.html")

    if request.form.get("checkbox"):
        session["remember_me"] = True
    
    session['logged_in'] = True
    session['username'] = username
    flash("Successfully logged in", "success")
    
    return redirect(url_for('index'))

@app.route('/dashboard/<username>', methods=["GET", "POST"])
def dashboard(username):
    with connect_sql.sqlcursor() as c:
        c.execute("SELECT accountID, username, money, kills, deaths, jobID, score, experience, wantedlevel,  \
            DATE_FORMAT(registerdate, '%%d %%M %%Y') as reg_date, \
            DATE_FORMAT(lastlogin, '%%d, %%M, %%Y at %%r') as last_log \
        FROM \
            accounts \
        WHERE \
            username=%s", username)
        results = c.fetchone()


    jobID = results['jobID']

    jobs = [
        "Drug Dealer",
        "Weapon Dealer",
        "Hitman",
        "Terrorist",
        "Rapist",
        "Mechanic"
    ]
    if jobID > len(jobs) or jobID < 0:
        jobName = "No job"
    else:
        jobName = jobs[jobID]
    
    return render_template("dashboard.html", results=results, jobName=jobName)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully logged out", "success")
    return redirect(url_for('index'))