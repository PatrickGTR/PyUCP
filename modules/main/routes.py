from flask import (
    Flask,
    render_template,
    request,session,
    url_for,
    redirect,
    flash,
    Blueprint,
    abort
)

from flask_paginate import (
    Pagination, 
    get_page_args
)

import pymysql
import hashlib


from modules.connect_sql import MySQL 
from modules.config import Config

from modules.functions import (
    retrieveAdmins, 
    isUserLoggedIn, 
    sendUserToHome
)

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return sendUserToHome()

@main.route('/home', 
    defaults={'page': 1}, 
    methods=["GET", "POST"]
)
@main.route("/home/<int:page>", methods=["GET", "POST"])
def home(page):

    """ Posts """

    with MySQL() as c:
        c.execute("SELECT * FROM posts")
        c.fetchall()
        num_rows = c.rowcount

    conf = Config()

    per_page = conf.PER_PAGE
    pagination = Pagination(page=1, per_page=per_page, total=num_rows, bs_version=4, alignment="center")
    page, per_page, offset = get_page_args()
                                           
    with MySQL() as c:
        c.execute(f"SELECT post_id, post_title, post_content, DATE_FORMAT(post_date, '%d, %M, %Y at %h:%i %p') as post_date, author_id FROM posts ORDER BY post_id DESC LIMIT {offset}, {per_page}")
        result_post = c.fetchall() 

    """ Account """
    # if user has ticked remember_me before, we set its session login to true and stop executing the code below.
    if(session.get("remember_me")):
        session["logged_in"] = True
        return render_template("index.html",
            active='home',
            pagination=pagination,
            news=result_post,
            admins=retrieveAdmins()
        )

    # if the method we get is not post, we send the user back to index.html
    if(request.method == "POST"):
        # set username variable to form input.
        # set password variable to password input.
        username = request.form.get("username")
        password = request.form.get("password")

        # run query, retrieve the accountID, password and hash from username variable.
        with MySQL() as c:
            c.execute("SELECT accountID, password, hash FROM accounts WHERE username = %s", username)
            accResult = c.fetchone()

        # if there is no result returned, we send the user a error message then redirect back to index.html
        if(accResult == None):
            flash("Invalid password or username, please try again.", "danger")
            return sendUserToHome()

        # we set retPassword and retSalt variable  to the password and hash we retrieved from the database.
        retPassword, retSalt = accResult["password"], accResult["hash"]
        # password variable will be sha256 hash and salt concatted together.
        password = hashlib.sha256(password.encode() + retSalt.encode()).hexdigest()

        # compare password, if password is the same, let the code continue else we return an error message and redirect the user back to index.html
        if password.upper() != retPassword:
            flash("Wrong password, please try again.", "danger")
            return sendUserToHome()

        # if user ticked the box, set the 'remember_me' session to true.
        if request.form.get("checkbox"):
            session.permanent = True # save session for 31 days, if remember me box is ticked.
            session["remember_me"] = True
        
        # if user logged in, we check in our admin database if they're admin, if they are, set session 'isAdmin' to true
        with MySQL() as c:
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
            active='home',
            pagination=pagination,
            news=result_post,
            admins=retrieveAdmins()
        )

@main.route("/dashboard/<int:accountid>", methods=["GET", "POST"])
def dashboard(accountid):
    # if user is not logged in, show him an error message saying he can't access this page.
    if(not isUserLoggedIn()):
        return abort(403)

    # if the session accountid is not the same as accountid passed to dashboard param then don't allow this process.
    if(session.get('accountid') != accountid):
        return abort(403)

    # retrieve players account data
    with MySQL() as c:
        c.execute(f"SELECT *,  \
            DATE_FORMAT(registerdate, '%d %M %Y') as reg_date, \
            DATE_FORMAT(lastlogin, '%d, %M, %Y at %r') as last_log \
        FROM \
            accounts \
        WHERE \
            accountID={accountid}")
        result_account = c.fetchone()
    
    # retrieve players skill data
    with MySQL() as c:
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
    with MySQL() as c:
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
        active='dashboard',
        item=result_item, 
        skill=result_skill,
        account=result_account, 
        admins=retrieveAdmins()
    )

@main.route("/logout")
def logout():
    session.clear()
    flash("You have successfully logged out", "success")
    return sendUserToHome()