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
    "nb_fields",
    Column(name="cloze",type="BOOLEAN"),
    Column(name="usn",type="INT"),
    Column(name="vers",type="TEXT"),
]
table = Table(name, columns)
def getTemplates(id):
    model = mw.col.models.get(id)
    if model:
        return model["tmpls"]
    return []

def oneLine(line):
    json, css, did, id, latexPost, latexPre, mod, name, req, sortf, tags, nb_tmpls, nb_fields, type, usn, vers = line
    oldModel = mw.col.models.get(id)
    templates = oldModel["tmpls"]
    fields = oldModel["flds"]
    model = dict(
        css = css,
        did = did,
        id = id,
        latexPre = latexPre,
        latexPost = latexPost,
        mod = mod,
        name = name,
        sortf = sortf,
        flds = fields,
        tmpls = templates,
        tags = json.loads (tags),
        type = 1 if type else 0,
        usn = usn,
        vers = json.loads(vers),
        tmpls = getTemplates(id)
    )
    if req is not None:
        model["req"] = json.loads(req)
    return id, model

def allLines(lines):
    if shouldDelete():
        models = dict()
    else:
        models = mw.col.models.models
    for line in lines:
        id, model = oneLine(line)
        models[id]=model
    mw.col.models.models = models
    mw.col.models.changed = True
    mw.col.models.flush()

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
                len(model["flds"]),
                int(model["type"])==1,#otherwise 0
                model["usn"],
                json.dumps(model["vers"])
            )
        except:
            raise
from ..meta import Data
data = Data(table, getRows, allLines)
