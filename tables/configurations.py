from ..db import *
import json
from aqt import mw
name="configurations"

columns = ([
    Column(name="json", type="TEXT")
    Column(name="name", type="text", unique= True),
    Column(name="maxTaken",type="int"),
    Column(name="timer",type="BOOLEAN"),
    Column(name="autoplay",type="BOOLEAN"),
    Column(name="replayq",type="BOOLEAN"),
    Column(name="mod",type="int"),
    Column(name="usn",type="int"),
    Column(name="dyn",type="BOOLEAN"),
    Column(name="id", type="int", primary=True)
]+
          [
              "new_delays",
              "ints",
              Column(name="initial_factor",type="NUMERIC"),
              "separate",
              Column(name="random",type="BOOLEAN"),
              Column(name="new_perDay",type="int"),
              Column(name="new_bury",type="BOOLEAN"),
          ]+
          [
              "lapse_delays",
              Column(name="mult",type="NUMERIC"),
              Column(name="minInt",type="NUMERIC"),
              Column(name="leechFails",type="INT"),
              Column(name="leechSuspend",type="BOOLEAN"),
          ]+
          [
              "review_perDay",
              Column(name="ease4",type="NUMERIC"),
              Column(name="fuzz",type="NUMERIC"),
              "minSpace",
              Column(name="ivlFct",type="NUMERIC"),
              Column(name="maxIvl",type="NUMERIC"),
              Column(name="review_bury",type="BOOLEAN"),
     ]
     )

table = Table(name, columns)

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
data = Data(name, columns, getRows)
