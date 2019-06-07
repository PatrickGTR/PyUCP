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

from struct import unpack

from flask_paginate import (
    Pagination,
    get_page_args
)

from modules.connect_sql import MySQL
from modules.config import Config

from modules.functions import (
    retrieveAdmins,
    isUserLoggedIn,
    sendUserToHome,
    getItemName,
    setUserLoggedIn
)

from modules.main.impl import (
    loginUser,
    retrieveUserData
)

main = Blueprint('main', __name__)

# Redirect user to /home directory.
@main.route("/")
def index():
    return sendUserToHome()

@main.route("/home/", methods=["GET", "POST"])
def home():
    """ Posts """

    conf = Config()

    per_page = conf.PER_PAGE
    page, per_page, offset = get_page_args()

    with MySQL() as c:
        c.execute("SELECT * FROM posts")
        c.fetchall()
        num_rows = c.rowcount

    pagination = Pagination(page=page, per_page=per_page, total=num_rows, bs_version=4, alignment="center")

    with MySQL() as c:
        c.execute(f"SELECT post_id, post_title, post_content, DATE_FORMAT(post_date, '%d, %M, %Y at %h:%i %p') as post_date, author_id FROM posts ORDER BY post_id DESC LIMIT {offset}, {per_page}")
        result_post = c.fetchall()

    """ Account """
    # if user has ticked remember_me before, we set its session login to true and stop executing the code below.
    if(session.get("remember_me")):
        setUserLoggedIn(True)
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

        loginUser(username, password)
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

    result_account, result_skill, result_item = retrieveUserData(accountid)

    return render_template("dashboard.html",
        active='dashboard',
        account=result_account,
        skill=result_skill,
        item=result_item,
        admins=retrieveAdmins()
    )

@main.route("/logout")
def logout():
    # if user is not logged in, show him an error message saying he can't access this page.
    if(not isUserLoggedIn()):
        return abort(403)

    session.clear()
    flash("You have successfully logged out", "success")
    return sendUserToHome()

@main.route("/search", methods=["GET", "POST"])
def search():
    if(request.method == "GET"):
        username = request.args.get("search")

        if(username == None):
            return render_template("search.html",
                username=username,
                active='search',
                admins=retrieveAdmins()
            )

        with MySQL() as c:
            c.execute("SELECT accountID FROM accounts WHERE username = %s", username)
            result = c.fetchone()

        if(result == None):
            flash("Invalid username, please try again.","danger")
            return redirect(url_for("main.search"))

        result_account, result_skill, result_item = retrieveUserData(result['accountID'])

        return render_template("search.html",
            active='search',
            account=result_account,
            skill=result_skill,
            item=result_item,
            admins=retrieveAdmins()
        )
    if(request.method == "POST"):
        # set username variable to form input.
        # set password variable to password input.
        username = request.form.get("username")
        password = request.form.get("password")

        loginUser(username, password)
        flash("Successfully logged in", "success")
    return redirect(url_for("main.search"));