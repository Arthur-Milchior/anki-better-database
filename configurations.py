from aqt import mw
name="configurations"

fields = ([
    ("name", "text UNIQUE"),
    ("maxTaken","int"),
    ("timer","BOOLEAN"),
    ("autoplay","BOOLEAN"),
    ("replayq","BOOLEAN"),
    ("mod","int"),
    ("usn","int"),
    ("dyn","BOOLEAN"),
    ("id", "int UNIQUE PRIMARY KEY")
]+
     [
         "new_delays",
         "ints",
         ("initial_factor","NUMERIC"),
         "separate",
         ("random","BOOLEAN"),
         ("new_perDay","int"),
         ("new_bury","BOOLEAN"),
     ]+
     [
         "review_perDay",
         ("ease4","NUMERIC"),
         ("fuzz","NUMERIC"),
         "minSpace",
         ("ivlFct","NUMERIC"),
         ("maxIvl","NUMERIC"),
         ("review_bury","BOOLEAN"),
     ]+
     [
         "lapse_delays",
         ("mult","NUMERIC"),
         ("minInt","NUMERIC"),
         ("leechFails","INT"),
         ("leechSuspend","BOOLEAN"),
        ])

def getRows():
    col = mw.col
    decks = col.decks.decks
    for option in decks:
        yield (
            option["name"],
            option["maxTaken"],
            int(option["timer"]) == 1,
            option["autoplay"],
            option["replayq"],
            option["mod"],
            option["usn"],
            option["dyn"],
            option["id"]
            option["new"]["delays"],
            option["new"]["ints"],
            option["new"]["initial_factor"],
            option["new"]["separate"],
            int(option["new"]["order"])==0,
            option["new"]["perDay"],
            option["new"]["bury"],
            option["review"]["perDay"],
            option["review"]["ease4"],
            option["review"]["fuzz"],
            option["review"]["minSpace"],
            option["review"]["ivlFct"],
            option["review"]["maxIvl"],
            option["review"]["bury"],
            option["lapse"]["delays"],
            option["lapse"]["mult"],
            option["lapse"]["minInt"],
            option["lapse"]["leechFails"],
            int(option["lapse"]["leechAction"])==0
           )
from meta import Data
Data(name, fields, getRows, end)
