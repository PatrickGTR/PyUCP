from flask import (
    Flask,
    render_template,
    request,session,
    url_for,
    redirect,
    flash
)

from flask_paginate import (
    Pagination, 
    get_page_args
)

import pymysql
import hashlib

from modules import (
    app, 
    connect_sql,
    functions
)

@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route('/home', 
    defaults={'page': 1}, 
    methods=["GET", "POST"]
)
@app.route("/home/<int:page>", methods=["GET", "POST"])
def home(page):

    """ Posts """

    with connect_sql.MySQL() as c:
        c.execute("SELECT * FROM posts")
        c.fetchall()
        num_rows = c.rowcount

    per_page = app.config.get('PER_PAGE')
    pagination = Pagination(page=1, per_page=per_page, total=num_rows, bs_version=4, alignment="center")
    page, per_page, offset = get_page_args()
                                           
    with connect_sql.MySQL() as c:
        c.execute(f"SELECT post_id, post_title, post_content, DATE_FORMAT(post_date, '%d, %M, %Y at %h:%i %p') as post_date, author_id FROM posts ORDER BY post_id DESC LIMIT {offset}, {per_page}")
        result_post = c.fetchall() 

    """ Account """
    # if user has ticked remember_me before, we set its session login to true and stop executing the code below.
    if(session.get("remember_me")):
        session["logged_in"] = True
        return render_template("index.html",
            pagination=pagination,
            news=result_post,
            admins=functions.retrieveAdmins()
        )

    # if the method we get is not post, we send the user back to index.html
    if(request.method == "POST"):
        # set username variable to form input.
        # set password variable to password input.
        username = request.form.get("username")
        password = request.form.get("password")

        # run query, retrieve the accountID, password and hash from username variable.
        with connect_sql.MySQL() as c:
            c.execute("SELECT accountID, password, hash FROM accounts WHERE username = %s", username)
            accResult = c.fetchone()

        # if there is no result returned, we send the user a error message then redirect back to index.html
        if(accResult == None):
            flash("Invalid password or username, please try again.", "danger")
            return redirect(url_for('home'))

        # we set retPassword and retSalt variable  to the password and hash we retrieved from the database.
        retPassword, retSalt = accResult["password"], accResult["hash"]
        # password variable will be sha256 hash and salt concatted together.
        password = hashlib.sha256(password.encode() + retSalt.encode()).hexdigest()

        # compare password, if password is the same, let the code continue else we return an error message and redirect the user back to index.html
        if password.upper() != retPassword:
            flash("Wrong password, please try again.", "danger")
            return redirect(url_for('home'))

        # if user ticked the box, set the 'remember_me' session to true.
        if request.form.get("checkbox"):
            session["remember_me"] = True
        
        # if user logged in, we check in our admin database if they're admin, if they are, set session 'isAdmin' to true
        with connect_sql.MySQL() as c:
            c.execute("SELECT adminLevel FROM admins WHERE userID = %s", accResult['accountID'])
            admResult = c.fetchone()

        if(admResult):
            if(admResult['adminLevel'] >= 1):
                session['isAdmin'] = True
        
        # if none of the error code above occured, set the session 'logged_in' to true and 'accountid' to the accountID from the database, show message to user that he logged in.
        session["logged_in"] = True
        session["accountid"] = accResult["accountID"]
        flash("Successfully logged in", "success")
    
    return render_template("index.html",
            pagination=pagination,
            news=result_post,
            admins=functions.retrieveAdmins()
        )

@app.route("/dashboard/<int:accountid>", methods=["GET", "POST"])
def dashboard(accountid):

    # retrieve players account data
    with connect_sql.MySQL() as c:
        c.execute(f"SELECT *,  \
            DATE_FORMAT(registerdate, '%d %M %Y') as reg_date, \
            DATE_FORMAT(lastlogin, '%d, %M, %Y at %r') as last_log \
        FROM \
            accounts \
        WHERE \
            accountID={accountid}")
        result_account = c.fetchone()
    
    # retrieve players skill data
    with connect_sql.MySQL() as c:
        c.execute(f"\
            SELECT \
                type.skill_id, type.skill_name, IFNULL(skill.value, 0) as value \
            FROM \
                skills_type AS type \
            LEFT JOIN \
                skills_player AS skill \
            ON \
                skill.fk_skill_id = type.skill_id AND \
                skill.fk_user_id = {accountid}")
        result_skill = c.fetchall()
    
    # retrieve players item data
    with connect_sql.MySQL() as c:
        c.execute(f"\
            SELECT \
                type.item_id, type.item_name, IFNULL(item.value, 0) as value \
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

# put into separated module (look onto using flask-blueprint)
@app.route("/news_write")
def news_write():
    # if the user is not signed in and logged in, disallow from accessing this link.
    if(functions.isPlayerLoggedIn() == 0):
        return redirect(url_for('home')) # TODO: Send to 403 instead of home.

    return render_template("news_write.html", 
        admins=functions.retrieveAdmins()
    )

@app.route("/news_edit/<int:postid>")
def news_edit(postid):
    # if the user is not signed in and logged in, disallow from accessing this link.
    if(not functions.isPlayerLoggedIn()):
        return redirect(url_for('home')) # TODO: Send to 403 instead of home.

    with connect_sql.MySQL() as c:
        c.execute("SELECT post_id, post_title, post_content FROM posts WHERE post_id = %s", postid)
        result = c.fetchone()

    return render_template("news_edit.html",
        post_data=result,
        admins=functions.retrieveAdmins() 
    )

@app.route("/write_success", methods=["GET", "POST"])
def write_success():
    # if the user is not logged in, disallow from accessing this link.
    if(not functions.isPlayerLoggedIn()):
        return redirect(url_for('home')) # TODO: Send to 403 instead of home.

    title = request.form.get('news_title') 
    content = request.form.get('news_message')
    author = session.get("accountid") 

    with connect_sql.MySQL() as c:
       c.execute("INSERT INTO posts (post_title, post_content, post_date, author_id) VALUES (%s, %s, NOW(), %s)", (title, content, author))

    flash("You have successfully posted the content", "success")
    return redirect(url_for('home'))

@app.route("/edit_success/<int:postid>", methods=["GET", "POST"])
def edit_success(postid):
    # if the user is not logged in, disallow from accessing this link.
    if(not functions.isPlayerLoggedIn()):
        return redirect(url_for('home')) # TODO: Send to 403 instead of home.
    
    title = request.form.get('news_title') 
    content = request.form.get('news_message')
    flash("You have successfully edited the content", "success")

    with connect_sql.MySQL() as c:
        c.execute("UPDATE posts SET post_content=%s, post_title=%s WHERE post_id=%s", (content, title, postid))

    return redirect(url_for('home'))

@app.route("/write_delete/<int:postid>", methods=["GET", "POST"])
def write_delete(postid):
    # if the user is not logged in, disallow from accessing this link.
    if(not functions.isPlayerLoggedIn()):
        return redirect(url_for('home')) # TODO: Send to 403 instead of home.
        
    with connect_sql.MySQL() as c:
        c.execute("DELETE FROM posts WHERE post_id=%s", postid)

    flash("You have successfully deleted the content", "success")
    return redirect(url_for('index'))