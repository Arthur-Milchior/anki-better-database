from aqt import mw
from .decks import data
import json
name= "models"
column=[
    ("json", "TEXT"),
    ("css","Text"),
    ("did","INTEGER REFERENCES decks (id) ON DELETE SET NULL"),
    ("id","INTEGER UNIQUE PRIMARY KEY"),
    ("latexPost","Text"),
    ("latexPre","Text"),
    ("mod","int"),
    ("name","Text"),
    ("req","TEXT"),
    ("sortf","int"),
    ("tags","TEXT"),
    "nb_tmpls",
    ("cloze","BOOLEAN"),
    ("usn","INT"),
    ("vers","TEXT"),
]


def getRows():
    models = mw.col.models.models
    for model in models.values():
        try:
            yield (
                json.dumps(model),
                model["css"],
                model["did"],
                model["id"],
                model["latexPost"],
                model["latexPre"],
                model["mod"],
                model["name"],
                json.dumps(model.get("req",None)),#absent for clozes
                model["sortf"],
                json.dumps(model["tags"]),
                len(model["tmpls"]),
                int(model["type"])==1,
                model["usn"],
                json.dumps(model["vers"])
            )
        except:
            raise
from ..meta import Data
data = Data(name, column, getRows)
