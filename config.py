from .debug import *
from aqt import mw
import os
from anki.db import DB
path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name
#The order is important in config.json because of references to other database.
localDb = None

def getLocalDb():
    global localDb
    if localDb is None:
        localDb = DB(f"{path}/clearer.{name}.sqlite3")
        if doDebug:
            localDb.echo= True
    return localDb

userOption = None
def getUserOption():
    global userOption
    if userOption is None:
        userOption = mw.addonManager.getConfig(__name__)
    return userOption

def update(_):
    global userOption
    userOption = None

mw.addonManager.setConfigUpdatedAction(__name__,update)

def considerTable(tableName):
    for table in getUserOption().get("tables"):
        if table["name"] == tableName:
            return table.get("consider",False)
    return False

def isTableInSameDb(table):
    return considerTable(table) or (addTableInAnki() and table in {"cards", "col", "graves", "notes", "revlog"})

def addTableInAnki():
    return False# getUserOption().get("use anki's database", False)

def shouldDelete():
    return getUserOption().get("deletion", False)

def getDb():
    if addTableInAnki():
        if doDebug:
            mw.col.db.echo = True
        return mw.col.db
    else:
        return getLocalDb()

def keepTable():
    keep = getUserOption().get("keep table", False)
    #debug(f"should we keep table: {keep}")
    return keep
