from ..db import *
from aqt import mw
from .models  import data
from .decks import data
import sys
import json

name= "template"
columns = [
    Column(name="json", type="TEXT"),
    Column(name="mid",type="INTEGER", reference= Reference("models", "id",  delete = cascade)),
    Column(name="ord",type="int"),
    Column(name="afmt",type="Text"),
    Column(name="bafmt",type="Text"),
    Column(name="qfmt",type="Text"),
    Column(name="bqfmt",type="Text"),
    Column(name="did",type="INTEGER", reference= Reference("models", "id",  delete = setNull)),
    Column(name="name",type="Text"),
]
table = Table(name, columns, ["ord","mid"], order = ["mid", "ord"])

def oneLine(line):
    json, mid, ord, afmt, bafmt, qfmt, bqfmt, did, name = line
    template = dict(
        ord = ord,
        afmt = afmt,
        bafmt = bafmt,
        qfmt = qfmt,
        bqfmt = bqfmt,
        did = did,
        name = nane,
    )
    return mid, ord, template

def allLines(lines):
    lastOrd = None
    lastMid = None
    lastModel = None
    listTemplates = []
    midOk = True
    for line in lines:
        mid,ord,template = oneLine(line)
        if lastMid == mid:
            if not midOk:
                continue
        else:
            endModel(lastModel, listTemplates)
            midOk = True
            lastOrd = -1
            lastMid = mid
            lastModel = mw.col.models.get(mid)
        if ord != lastOrd+1:
            print (f"""The template in ord {lastOrd+1} is missing while {ord} is present,
            for model {mid}:{fn["name"]}""", filde = sys.stderr)
            midOk = False
            continue
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
        mid = model["id"]
        if "tmpls" in model:
            for template in model["tmpls"]:
                yield (
                    json.dumps(template),
                    mid,
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

from ..meta import Data
data = Data(table, getRows, allLines)
