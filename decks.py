from aqt import mw
name="decks"

l = ["newToday",
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
     ("mid",              "INTEGER")
]


def getRows():
    col = mw.col
    decks = col.decks.decks
    for deck in decks:
        yield (deck["newToday"],
               deck["revToday"],
               deck["lrnToday"],
               deck["timeToday"],
               deck["conf"],
               deck["usn"],
               deck["desc"],
               deck["dyn"],
               deck["collapsed"],
               deck["extendNew"],
               deck["extendRev"],
               deck["name"],
               deck["browserCollapsed"],
               deck["id"],
               deck["mod"],
               deck["mid"])
from meta import Data
Data(name, fields, getRows)
