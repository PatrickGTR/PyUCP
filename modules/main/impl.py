from flask import (
    session,
    flash,
    request
)

from modules.functions import (
    sendUserToHome,
    setUserLoggedIn
)

from modules.connect_sql import MySQL
import hashlib

def retrieveUserData(accountid: int):
    # retrieve player account data
    with MySQL() as c:
        c.execute(
        """
        SELECT *,
            DATE_FORMAT(registerdate, "%%d %%M %%Y") as reg_date,
            DATE_FORMAT(lastlogin, "%%d, %%M, %%Y at %%r") as last_log
        FROM
            accounts
        WHERE
            accountID = %s
        """, (accountid))
        account = c.fetchone()

    # retrieve player skill data
    with MySQL() as c:
        c.execute(
            """
            SELECT
                type.skill_id, type.skill_name, IFNULL(skill.value, 0) as value
            FROM
                skills_type AS type
            LEFT JOIN
                skills_player AS skill
            ON
                skill.fk_skill_id = type.skill_id
            AND
                skill.fk_account_id = %s
            """, (accountid))
        skill = c.fetchall()

    # retrieve player item data
    with MySQL() as c:
        c.execute(
            """
            SELECT
                type.item_id, type.item_name, IFNULL(item.value, 0) as value
            FROM
                item_type AS type
            LEFT JOIN
                item_players AS item
            ON
                item.fk_item_id = type.item_id
            AND
                item.fk_account_id = %s
            """, (accountid))
        item = c.fetchall()
        return account, skill, item


def loginUser(username: str, password: str):
    # run query, retrieve the accountID, password and salt from username variable.
    with MySQL() as c:
        c.execute("SELECT accountID, password, salt FROM accounts WHERE username = %s", username)
        accResult = c.fetchone()

    # if there is no result returned, we send the user a error message then redirect back to index.html
    if(accResult == None):
        return 0
        ##flash("Invalid password or username, please try again.", "danger")
        ##return sendUserToHome()

    # we set retPassword and retSalt variable  to the password and hash we retrieved from the database.
    retPassword, retSalt = accResult["password"], accResult["salt"]
    # password variable will be sha256 hash and salt concatted together.
    password = hashlib.sha256(password.encode() + retSalt.encode()).hexdigest()

    # compare password, if password is the same, let the code continue else we return an error message and redirect the user back to index.html
    if password.upper() != retPassword:
        return 1
        ##flash("Wrong password, please try again.", "danger")
        ##return sendUserToHome()

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
    setUserLoggedIn(True)
    session["accountid"] = accResult["accountID"]
    return 2
