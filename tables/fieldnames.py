from ..db import *
from aqt import mw
import json

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

table = Table(name, columns, ["ord","mid"])
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
    return fn, mid


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
data = Data(name, column, getRows, end)
