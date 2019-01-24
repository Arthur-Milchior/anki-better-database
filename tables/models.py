from ..db import *
from aqt import mw
from .decks import data
import json

name= "models"
columns=[
    Column(name="json", type="TEXT"),
    Column(name="css",type="Text"),
    Column(name="did",type="INTEGER", references= Reference(column="decks", table="id", delete= setNull, update = cascade)),
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
def oneLine(line):
    json, css, did, id, latexPost, latexPre, mod, name, req, sortf, tags, tmpls, type, usn, vers = line
    models = dict(
        css = css,
        did = did,
        id = id,
        latexPre = latexPre,
        latexPost = latexPost,
        mod = mod,
        name = name,
        sortf = sortf,
        tags = json.loads (tags),
        type = 1 if type else 0,
        usn = usn,
        vers = json.loads(vers)
    )
    if req is not None:
        models["req"] = json.loads(req)
    #todo: tmpls

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
                int(model["type"])==1,#otherwise 0
                model["usn"],
                json.dumps(model["vers"])
            )
        except:
            raise
from ..meta import Data
data = Data(name, column, getRows)
