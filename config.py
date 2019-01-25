import aqt
from .debug import *
from aqt import mw
import os
from anki.db import DB
path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name

localDb = None
def getLocalDb():
    global localDb
    if localDb is None:
        localDb = DB(f"{path}/clearer.{name}.sqlite3")
    return localDb

userOption = None
def getUserOption():
    global userOption
    if userOption is None:
        userOption = aqt.mw.addonManager.getConfig(__name__)
    return userOption

def update(_):
    global userOption
    userOption = None

mw.addonManager.setConfigUpdatedAction(__name__,update)

def considerTable(table):
    return table in getUserOption().get("tables")

def isTableInSameDb(table):
    return considerTable(table) or (addTableInAnki() and table in {"cards", "col", "graves", "notes", "revlog"})

def addTableInAnki():
    return getUserOption().get("use anki's database", False)
def shouldDelete():
    return getUserOption().get("deletion", False)

def getDb():
    if addTableInAnki():
        return mw.col.db
    else:
        return getLocalDb()

def keepTable():
    keep = getUserOption().get("keep table", False)
    #debug(f"should we keep table: {keep}")
    return keep
