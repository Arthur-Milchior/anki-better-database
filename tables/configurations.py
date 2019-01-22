import json
from aqt import mw
name="configurations"

fields = ([
    ("json", "TEXT"),
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
              "lapse_delays",
              ("mult","NUMERIC"),
              ("minInt","NUMERIC"),
              ("leechFails","INT"),
              ("leechSuspend","BOOLEAN"),
          ]+
          [
              "review_perDay",
              ("ease4","NUMERIC"),
              ("fuzz","NUMERIC"),
              "minSpace",
              ("ivlFct","NUMERIC"),
              ("maxIvl","NUMERIC"),
              ("review_bury","BOOLEAN"),
     ]
     )

def getRows():
    col = mw.col
    configurations = col.decks.allConf()
    #print(f"Decks are {decks}")
    for configuration in configurations:
        yield (
            json.dumps(configuration),
            configuration["name"],
            configuration["maxTaken"],
            int(configuration["timer"]) == 1,
            configuration["autoplay"],
            configuration["replayq"],
            configuration["mod"],
            configuration["usn"],
            configuration["dyn"],
            configuration["id"],
            json.dumps(configuration["new"]["delays"]),
            json.dumps(configuration["new"]["ints"]),
            configuration["new"]["initialFactor"],
            configuration["new"]["separate"],
            int(configuration["new"]["order"])==0,
            configuration["new"]["perDay"],
            configuration["new"]["bury"],
            json.dumps(configuration["lapse"]["delays"]),
            configuration["lapse"]["mult"],
            configuration["lapse"]["minInt"],
            configuration["lapse"]["leechFails"],
            int(configuration["lapse"]["leechAction"])==0,
            json.dumps(configuration["rev"]["perDay"]),
            configuration["rev"]["ease4"],
            configuration["rev"]["fuzz"],
            configuration["rev"]["minSpace"],
            configuration["rev"]["ivlFct"],
            configuration["rev"]["maxIvl"],
            configuration["rev"]["bury"],
           )
from ..meta import Data
data = Data(name, fields, getRows)
