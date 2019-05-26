

from flask import session, Blueprint, url_for, redirect
import pymysql

from modules.connect_sql import MySQL

funcs = Blueprint('funcs', __name__)

account_data = {
    "jobs": {
        0: "Drug Dealer",
        1: "Weapon Dealer",
        2: "Hitman",
        3: "Terrorist", 
        4: "Rapist",
        5: "Mechanic"
    },
    "skills":{
        0: "Players Raped",
        1: "Been Raped",
        2: "Players Robbed",
        3: "Been Robbed",
        4: "Stores Robbed",
        5: "Times Escaped Cuffs",
        6: "Players Arrested",
        7: "Times Been Arrested"
    },
    "items": {
        0: "Weed",
        1: "Crack",
        2: "Rope",
        3: "Lockpick",
        4: "Scissors",
        5: "Condoms",
        6: "Wallet",
        7: "C-4"
    }
}
def sendUserToHome():
    return redirect(url_for("main.home"))

def setUserLoggedIn(status: bool):
    session['logged_in'] = status

## app.template_global allows 
## the functions below to be used in our .html files.

@funcs.app_template_global()
def retrieveNameFromID(accountid):
    with MySQL() as c: 
        c.execute(f"SELECT username FROM accounts WHERE accountid={accountid}")
        result = c.fetchone()   
    return result["username"] 

@funcs.app_template_global()
def getJobName(jobid):
    jobName = account_data.get("jobs").get(jobid) 
    return jobName 

@funcs.app_template_global()
def getSkillName(skillid):
    skillName = account_data.get("skills").get(skillid) 
    return skillName 

@funcs.app_template_global()
def getItemName(itemid):
    itemName = account_data.get("items").get(itemid) 
    return itemName 

@funcs.app_template_global()
def retrieveAdmins():
    with MySQL() as c:
        c.execute("SELECT userID, adminLevel FROM admins")
        results = c.fetchall()
    return results
    
@funcs.app_template_global()
def isUserLoggedIn():
    if(session.get('logged_in') == None):
        return False
    else:
        return True

