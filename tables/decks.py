from ..db.db import *
from ..db.columns import *
from ..debug import *
import json
from aqt import mw
name="decks"

columns = [
    Column(name="json", type="TEXT"),
    "newToday",
    "revToday",
    "lrnToday",
    "timeToday",
    "conf",
    "usn",
    "descr",# r added, because desc means descending
    "dyn",
    Column(name="collapsed", type="BOOLEAN"),
    Column(name="extendNew", type="integer"),
    Column(name="extendRev", type="integer"),
    Column(name="name", type="TEXT", unique=True),
    Column(name="browserCollapsed", type="BOOLEAN"),
    Column(name="id", type="integer", primary=True),
    Column(name="mod", type="integer")
]

def oneLine(line):
    (json_, newToday, revToday, lrnToday, timeToday, conf, usn, desc, dyn, collapsed, extendNew, extendRev, name, browserCollapsed, id, mod) = line
    deck = dict(
        newToday = json.loads(newToday),
        revToday = json.loads(revToday),
        lrnToday = json.loads(lrnToday),
        timeToday = json.loads(timeToday),
        usn = usn,
        desc = desc,
        dyn = dyn,
        collapsed = collapsed,
        name = name,
        id = id,
        mod = mod
        )
    if conf is not None:
        deck["conf"] = conf
    if extendNew is not None:
        deck["extendNew"] = extendNew
    if extendRev is not None:
        deck["extendRev"] = extendRev
    if browserCollapsed is not None:
        deck["browserCollapsed"] = browserCollapsed
    return id, deck

def allLines(lines):
    if shouldDelete():
        mw.col.decks.decks = dict()
    d = mw.col.decks.decks
    for line in lines:
        id, deck = oneLine(line)
        d[str(id)] = deck
    mw.col.decks.flush()



def getRows():
    col = mw.col
    decks = col.decks.decks
    #debug(f"Decks is {decks}")
    for deck in decks.values():
        #debug(f"Deck is {deck}")
        yield (
            json.dumps(deck),
            json.dumps(deck["newToday"]),
            json.dumps(deck["revToday"]),
            json.dumps(deck["lrnToday"]),
            json.dumps(deck["timeToday"]),
            deck.get("conf",None),
            deck["usn"],
            deck["desc"],
            deck["dyn"],
            deck["collapsed"],
            deck.get("extendNew",None),
            deck.get("extendRev",None),
            deck["name"],
            deck.get("browserCollapsed",None),
            deck["id"],
            deck["mod"])
table = Table(name, columns, getRows, allLines)
