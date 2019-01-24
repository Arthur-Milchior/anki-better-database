from ..db import *
from aqt import mw
from .decks import data
import json

name= "models"
columns=[
    Column(name="json", type="TEXT"),
    Column(name="css",type="Text"),
    Column(name="did",type="INTEGER", references= Reference(column="decks", table="id", delete= setNull)),
    Column(name="id",type="INTEGER", primary=TRUE),
    Column(name="latexPost",type="Text"),
    Column(name="latexPre",type="Text"),
    Column(name="mod",type="int"),
    Column(name="name",type="Text"),
    Column(name="req",type="TEXT"),
    Column(name="sortf",type="int"),
    Column(name="tags",type="TEXT"),
    "nb_tmpls",
    Column(name="cloze",type="BOOLEAN"),
    Column(name="usn",type="INT"),
    Column(name="vers",type="TEXT"),
]
table = Table(name, columns)


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
