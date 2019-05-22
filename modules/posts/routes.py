from flask import (
    render_template, 
    redirect, 
    url_for, 
    session,
    request, 
    flash, 
    Blueprint, 
    abort
)

from modules.functions import (
    isUserLoggedIn, 
    retrieveAdmins, 
    sendUserToHome
)

from modules.connect_sql import MySQL

posts = Blueprint('posts', __name__)

@posts.route("/news_write")
def news_write():
    # if the user is not signed in and logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)

    return render_template("news_write.html", 
        admins=retrieveAdmins()
    )

@posts.route("/news_edit/<int:postid>")
def news_edit(postid):
    # if the user is not signed in and logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)

    with MySQL() as c:
        c.execute("SELECT post_id, post_title, post_content FROM posts WHERE post_id = %s", postid)
        result = c.fetchone()

    return render_template("news_edit.html",
        post_data=result,
        admins=retrieveAdmins() 
    )

@posts.route("/write_success", methods=["GET", "POST"])
def write_success():
    # if the user is not logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)

    title = request.form.get('news_title') 
    content = request.form.get('news_message')
    author = session.get("accountid") 

    with MySQL() as c:
       c.execute("INSERT INTO posts (post_title, post_content, post_date, author_id) VALUES (%s, %s, NOW(), %s)", (title, content, author))

    flash("You have successfully posted the content", "success")
    return sendUserToHome()

@posts.route("/edit_success/<int:postid>", methods=["GET", "POST"])
def edit_success(postid):
    # if the user is not logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)
    
    title = request.form.get('news_title') 
    content = request.form.get('news_message')
    flash("You have successfully edited the content", "success")

    with MySQL() as c:
        c.execute("UPDATE posts SET post_content=%s, post_title=%s WHERE post_id=%s", (content, title, postid))

    return sendUserToHome()

@posts.route("/write_delete/<int:postid>", methods=["GET", "POST"])
def write_delete(postid):
    # if the user is not logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)
        
    with MySQL() as c:
        c.execute("DELETE FROM posts WHERE post_id=%s", postid)

    flash("You have successfully deleted the content", "success")
    return sendUserToHome()