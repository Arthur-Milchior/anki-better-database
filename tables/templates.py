from ..db.db import *
from ..db.columns import *
from aqt import mw
from ..debug import *
import sys
import json

name= "templates"
columns = [
    Column(name="json", type="TEXT"),
    Column(name="model",type="text", reference= Reference("models", "name",  onDelete = cascade, update = cascade)),
    Column(name="ord",type="int"),
    Column(name="afmt",type="Text"),
    Column(name="bafmt",type="Text"),
    Column(name="qfmt",type="Text"),
    Column(name="bqfmt",type="Text"),
    Column(name="did",type="integer", reference= Reference("models", "id",  onDelete = setNull, update = cascade)),
    Column(name="name",type="Text"),
]


def oneLine(line):
    json_, modelName, ord, afmt, bafmt, qfmt, bqfmt, did, name = line
    template = dict(
        ord = ord,
        afmt = afmt,
        bafmt = bafmt,
        qfmt = qfmt,
        bqfmt = bqfmt,
        did = did,
        name = name,
    )
    return modelName, ord, template

def allLines(lines):
    lastModelName = None
    for line in lines:
        debug(f"""
------
Considering line: «{line}»""")
        modelName,ord,template = oneLine(line)
        if lastModelName == modelName:
            debug("Same modelName")
            if not lastModelOk:
                debug("not ok, thus continue")
                continue
        else:
            debug("New modelName")
            listTemplates = []
            lastModelName = modelName
            lastModel = mw.col.models.byName(modelName)
            endModel(lastModel, listTemplates)
            lastModelOk = True
            lastOrd = -1
            if lastModel is None:
                thisModelOk = False
                print(f"""Template {ord}:{template["name"]} should belong in model {lastModelName} which does not exists.""", file = sys.stderr)
                continue
        if ord != lastOrd+1:
            if template is None:
                debug("template is None")
            print (f"""The template in ord {lastOrd+1} is missing while {ord}:{template["name"]} is present, for model {lastModel["id"]}:{modelName}""", file = sys.stderr)
            lastModelOk = False
            continue
        lastOrd = ord
        listTemplates.append(template)
    endModel(lastModel, listTemplates)
    mw.col.models.flush()

def endModel(model, listTemplates):
    if model is None:
        return
    model["tmpls"] = listTemplates
    mw.col.models.save(model)


def getRows():
    models = mw.col.models.models
    for model in models.values():
        modelName = model["name"]
        if "tmpls" in model:
            for template in model["tmpls"]:
                yield (
                    json.dumps(template),
                    modelName,
                    template["ord"],
                    template["afmt"],
                    template["bafmt"],
                    template["qfmt"],
                    template["bqfmt"],
                    template["did"],
                    template["name"],
                )
        else:
            print(f"No tmpls in {model}", file = sys.stderr)

table = Table(name, columns, getRows, allLines, uniques = [["ord","model"],["name","model"]], order = ["model", "ord"])
