

from flask import session

from modules import (
    app, 
    connect_sql
)

import pymysql

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

## app.template_global allows 
## the functions below to be used in our .html files.

@app.template_global()
def retrieveNameFromID(accountid):
    with connect_sql.MySQL() as c: 
        c.execute(f"SELECT username FROM accounts WHERE accountid={accountid}")
        result = c.fetchone()
    return result["username"]

@app.template_global()
def getJobName(jobid):
    jobName = account_data.get("jobs").get(jobid)
    return jobName

@app.template_global()
def getSkillName(skillid):
    skillName = account_data.get("skills").get(skillid)
    return skillName

@app.template_global()
def getItemName(itemid):
    itemName = account_data.get("items").get(itemid)
    return itemName

@app.template_global()
def retrieveAdmins():
    with connect_sql.MySQL() as c:
        c.execute("SELECT userID, adminLevel FROM admins")
        results = c.fetchall()
    return results
    
@app.template_global()
def isPlayerLoggedIn():
    if(session.get('logged_in') is None):
        return False
    else:
        return True

