from flask import (
    render_template,
    redirect,
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

from modules.posts.impl import (
    writePost,
    editPost,
    updatePost,
    deletePost,
)

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

    result = editPost(postid)
    return render_template("news_edit.html",
        post_data=result,
        admins=retrieveAdmins()
    )

@posts.route("/write_success", methods=["POST"])
def write_success():
    # if the user is not logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)

    title = request.form.get('news_title')
    content = request.form.get('news_message')
    author = session.get("accountid")

    writePost(title, content, author)

    flash("You have successfully posted the content", "success")
    return sendUserToHome()

@posts.route("/edit_success/<int:postid>", methods=["GET", "POST"])
def edit_success(postid):
    # if the user is not logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)

    title = request.form.get('news_title')
    content = request.form.get('news_message')

    updatePost(title, content, postid)

    flash("You have successfully edited the content", "success")
    return sendUserToHome()

@posts.route("/write_delete/<int:postid>", methods=["GET", "POST"])
def write_delete(postid):
    # if the user is not logged in, disallow from accessing this link.
    if(not isUserLoggedIn()):
        return abort(403)

    deletePost(postid)

    flash("You have successfully deleted the content", "success")
    return sendUserToHome()