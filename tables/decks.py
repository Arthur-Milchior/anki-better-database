import json
from aqt import mw
name="decks"

columns = [
    ("json", "TEXT"),
    "newToday",
    "revToday",
    "lrnToday",
    "timeToday",
    "conf",
    "usn",
    "descr",# r added, because desc means descending
    "dyn",
    ("collapsed",        "BOOLEAN"),
    ("extendNew" ,       "INTEGER"),
    ("extendRev"  ,      "INTEGER"),
    ("name",             "TEXT    UNIQUE"),
    ("browserCollapsed", "BOOLEAN"),
    ("id",               "INTEGER UNIQUE  PRIMARY KEY"),
    ("mod",              "INTEGER"),
]


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
