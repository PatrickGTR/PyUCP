from flask import (
    Flask,
    render_template,
    request,session,
    url_for,
    redirect,
    flash
)

from modules import (
    app, 
    connect_sql,
    functions
)

import pymysql
import hashlib

@app.route("/", methods=["GET", "POST"])
def index():
    
    if(session.get("remember_me")):
        session["logged_in"] = True
        username = session["username"]
        return render_template("index.html", 
            admins=functions.retrieveAdmins()
        )

    if(request.method != "POST"):
        return render_template("index.html", 
            admins=functions.retrieveAdmins()
        )

    username = request.form.get("username")
    password = request.form.get("password")

    with connect_sql.MySQL() as c:
        c.execute("SELECT accountID, password, hash FROM accounts WHERE username=%s", username)
        results = c.fetchone()

    if not results:
        flash("Invalid password or username, please try again.", "danger")
        return render_template("index.html", 
            admins=functions.retrieveAdmins()
        )

    retPassword, retSalt = results["password"], results["hash"]
    password = hashlib.sha256(password.encode() + retSalt.encode()).hexdigest()

    if password.upper() != retPassword:
        flash("Wrong password, please try again.", "danger")
        return render_template("index.html", 
            admins=functions.retrieveAdmins()
        )

    if request.form.get("checkbox"):
        session["remember_me"] = True
    
    session["logged_in"] = True
    session["username"] = results["accountID"]
    flash("Successfully logged in", "success")
    
    return redirect(url_for("index"))

@app.route("/dashboard/<int:accountid>", methods=["GET", "POST"])
def dashboard(accountid):
    with connect_sql.MySQL() as c:
        c.execute(f"SELECT *,  \
            DATE_FORMAT(registerdate, '%d %M %Y') as reg_date, \
            DATE_FORMAT(lastlogin, '%d, %M, %Y at %r') as last_log \
        FROM \
            accounts \
        WHERE \
            accountID={accountid}")
        result_account = c.fetchone()
    
    with connect_sql.MySQL() as c:
        c.execute(f"\
            SELECT \
                type.skill_id, type.skill_name, skill.value \
            FROM \
                skills_type AS type \
            LEFT JOIN \
                skills_player AS skill \
            ON \
                skill.fk_skill_id = type.skill_id AND \
                skill.fk_user_id = {accountid}")
        result_skill = c.fetchall()
    
    with connect_sql.MySQL() as c:
        c.execute(f"\
            SELECT \
                type.item_id, type.item_name, item.value \
            FROM \
                item_type AS type \
            LEFT JOIN \
                item_players AS item \
            ON \
                item.fk_item_id = type.item_id AND \
                item.fk_user_id = {accountid}")
        result_item = c.fetchall()

    return render_template("dashboard.html", 
        item=result_item, 
        skill=result_skill,
        account=result_account, 
        admins=functions.retrieveAdmins()
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("You have successfully logged out", "success")
    return redirect(url_for("index"))
