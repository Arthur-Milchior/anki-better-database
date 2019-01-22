from aqt import mw
import json

name= "fieldnames"
column=[
    ("name" ,  "TEXT"),
    ("ord"   , "INT"),
    ("mid"    ,"INT"),
    ("font"   ,"TEXT"),
    ("media"),
    ("rtl"),
    ("sticky" ,"BOOLEAN"),
    ("size"   ,"INTEGER"),
]

end = """ UNIQUE (
        ord,
        mid
    )"""

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
