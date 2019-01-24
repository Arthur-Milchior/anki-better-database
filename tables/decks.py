from ..db import *
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
    Column(name="extendNew", type="INTEGER"),
    Column(name="extendRev", type="INTEGER"),
    Column(name="name", type="TEXT",unique=True),
    Column(name="browserCollapsed", type="BOOLEAN"),
    Column(name="id", type="INTEGER", PRIMARY=TRUE),
    Column(name="mod", type="INTEGER")
]

table = Table(name, columns)

def getRows():
    col = mw.col
    decks = col.decks.decks
    #print(f"Decks is {decks}")
    for deck in decks.values():
        #print(f"Deck is {deck}")
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
from ..meta import Data
data = Data(name, columns, getRows)
