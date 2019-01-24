from ..db import *
from aqt import mw
import json

name= "fieldnames"
column=[
    Column(name="name", type="TEXT"),
    Column(name="ord", type="INT"),
    Column(name="mid", type="INT"),
    Column(name="font", type="TEXT"),
    Column(name="media"),
    Column(name="rtl"),
    Column(name="sticky",type="BOOLEAN"),
    Column(name="size",type="INTEGER"),
]

table = Table(name, columns, ["ord","mid"])

def getRows():
    col = mw.col
    models = col.models.models
    for model in models.values():
        modelId = model["id"]
        for field in model["flds"]:
            yield (
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
