from aqt import mw

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
    execute(create_query)
    col = mw.col
    models = col.models.models
    for model in models:
        modelId = model["id"]
        for field in model["flds"]:
            yeld (field["name"], int(field["ord"]), modelId, field["font"], field["media"], field["rtl"], field["sticky"], field["size"])
from meta import Data
Data(name, column, getRows, end)
