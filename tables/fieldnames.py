from ..db.db import *
from ..db.columns import *
from ..debug import *
from aqt import mw
import json
import sys

name= "fieldnames"
columns=[
    Column(name="json", type="TEXT"),
    Column(name="name", type="TEXT"),
    Column(name="ord", type="INT"),
    Column(name="model", type="TEXT", reference = Reference(column = "models", table="name", onDelete = setNull, update=cascade)),
    Column(name="font", type="TEXT"),
    Column(name="media"),
    Column(name="rtl"),
    Column(name="sticky",type="BOOLEAN"),
    Column(name="size",type="integer"),
]

def oneLine(line):
    json_, name, ord, modelName, font, media, rtl, sticky, size = line
    fn = dict(
        name = name,
        ord = ord,
        font = font,
        media = json.loads(media),
        rtl = rtl,
        sticky = sticky,
        size = size
    )
    return fn, modelName, ord

def endThisModel(model, fields):
    if model is None:
        return
    model["flds"] = fields
    mw.col.models.save(model)

def allLines(lines):
    lastModelName = None
    lastOrd = None
    lastModel = None
    thisModelOk = True
    listFields = []
    for line in lines:
        debug(f"""
------
Considering line: «{line}»""")
        fn, modelName, ord= oneLine(line)
        if modelName == lastModelName:
            debug("Same modelName")
            if not thisModelOk:
                debug("not ok, thus continue")
                continue
        else:
            debug("New modelName")
            endThisModel(lastModel,listFields)
            lastModelName = modelName
            lastOrd = -1
            lastModel = mw.col.models.byName(modelName)
            if lastModel is None:
                thisModelOk = False
                print(f"""Field name {ord}:{fn["name"]} should belong in model {modelName} which does not exists.""", file = sys.stderr)
                continue
            thisModelOk = True
            listFields = []
        if ord != lastOrd+1:
            if fn is None:
                debug("fn is None")
            print(f"""The field name in ord {lastOrd+1} is missing while the field name {ord}:{fn["name"]} is present, for model {lastModel["id"]}:{lastModel["name"]}""", file = sys.stderr)
            thisModelOk = False
            continue
        lastOrd = ord
        listFields.append(fn)
    endThisModel(lastModel,listFields)
    mw.col.models.flush()


def getRows():
    col = mw.col
    models = col.models.models
    for model in models.values():
        modelId = model["id"]
        modelName = model["name"]
        for field in model["flds"]:
            yield (
                json.dumps(field),
                field["name"],
                int(field["ord"]),
                modelName,
                field["font"],
                json.dumps(field["media"]),
                field["rtl"],
                field["sticky"],
                field["size"])

table = Table(name, columns, getRows, allLines, uniques = [["ord","model"],["name","model"],], order = ["model","ord"])

def getFieldOrd(name,modelName):
    condition = " where name = ? and model = ?"
    return table.scalar("ord", condition, name, modelName)
    
