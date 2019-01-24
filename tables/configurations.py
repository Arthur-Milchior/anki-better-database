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

def oneLine(line):
    json, name, maxTaken, timer, autoPlay, replayQ, mod, usn, dyn, id, new_delay, ints, initialFactor, separate, random, new_perDay, new_bury, lapse_delays, mult, minInt, leechFails, leechSuspend, review_perDay, ease4, fuzz, minSpace, ivlFct, maxIvl, review_bury = line
    new = dict(
        delays = delays,
        ints = ints,
        initialFactor = initialFactor,
        separate = separate,
        order = 0 if random else 1,
        perDay = new_perDay,
    bury = bury)
    lapse = dict(
        delays = json.loads(delays),
        mult = mult,
        minInt = minInt,
        leechFails = leechFails,
        leechAction = 0 if leechSuspend else 1
    )
    rev = dict(
        perdDay = json.loads(review_perDay),
        ease4 = ease4,
        fuzz = fuzz,
        minSpace = minSpace,
        ivlFct = ivlFct,
        maxIvl = maxIvl,
        bury = bury
    )
    conf = dict(
        name = name,
        maxTaken = maxTaken,
        timer = 1 if timer else 0,
        autoplay = autoplay,
        replayQ = replayQ,
        mod = mod,
        usn = usn,
        dyn = dyn,
        id = id,
        new = new,
        lapse = lapse,
        rev = rev
    )
    return conf

from ..meta import Data
data = Data(table, getRows)
