from ..db import *
from aqt import mw
import json
import sys

name= "fieldnames"
column=[
    Column(name="json", type="TEXT"),
    Column(name="name", type="TEXT"),
    Column(name="ord", type="INT"),
    Column(name="mid", type="INT", references = Reference(column = "models", table="id", delete = setNull, update=cascade)),
    Column(name="font", type="TEXT"),
    Column(name="media"),
    Column(name="rtl"),
    Column(name="sticky",type="BOOLEAN"),
    Column(name="size",type="INTEGER"),
]

def oneLine(line):
    json, name, ord, mid, font, media, rtl, sticky, size = line
    fn = dict(
        name = name,
        ord = ord,
        font = font,
        media = json.loads(media),
        rtl = rtl,
        sticky = sticky,
        size = size
    )
    return fn, mid, ord

def endMid(model, fields):
    if model is None:
        return
    model["flds"] = fields
    mw.col.models.save(model)

table = Table(name, columns, ["ord","mid"], order = ["mid"], order = ["mid","ord"])
def allLines(lines):
    lastMid = None
    lastOrd = None
    lastModel = None
    midOk = True
    listFields = []
    for line in lines:
        fn, mid, ord= oneLine(line)
        if mid == lastMid:
            if not midOk:
                continue
        else:
            midOk = True
            endMid(lastModel,listFields)
            lastMid = mid
            lastOrd = -1
            lastModel = mw.col.models.get(mid)
            listFields = []
        if ord != lastOrd+1:
            print (f"""The field in ord {lastOrd+1} is missing while {ord} is present, for model {mid}:{fn["name"]}""", filde = sys.stderr)
            midOk = False
            continue
        listFields.append(fn)
    endMid(lastModel,listFields)
    mw.col.models.flush()


def getRows():
    col = mw.col
    models = col.models.models
    for model in models.values():
        modelId = model["id"]
        for field in model["flds"]:
            yield (
                json.dumps(field),
                field["name"],
                int(field["ord"]),
                modelId,
                field["font"],
                json.dumps(field["media"]),
                field["rtl"],
                field["sticky"],
                field["size"])
from ..meta import Data
data = Data(table, getRows, allLines)
