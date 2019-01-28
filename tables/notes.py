from ..db.db import *
from ..db.columns import *
from aqt import mw
import json
from anki.find import Finder

name= "notes"
columns=[
    Column(name="id", type="integer", primary=True),
    Column(name="guid",type="int", unique=True),
    Column(name="mod",type="int"),
    Column(name="model",type="text", reference= Reference("models", "name",  onDelete = cascade, update = cascade)),
    Column(name="usn",type="INT"),
]

# def oneLine(line):
#     json_, css, deckName, id, latexPost, latexPre, mod, name, req, sortf, tags, nb_tmpls, nb_fields, type, usn, vers = line
#     oldModel = mw.col.models.get(id)
#     templates = oldModel["tmpls"]
#     fields = oldModel["flds"]
#     did = mw.col.decks.byName(deckName)
#     model = dict(
#         css = css,
#         did = did,
#         id = id,
#         latexPre = latexPre,
#         latexPost = latexPost,
#         mod = mod,
#         name = name,
#         sortf = sortf,
#         flds = fields,
#         tags = json.loads (tags),
#         type = 1 if type else 0,
#         usn = usn,
#         vers = json.loads(vers),
#         tmpls = getTemplates(id)
#     )
#     if req is not None:
#         model["req"] = json.loads(req)
#     return id, model

def allLines(lines):
    pass
#     if shouldDelete():
#         models = dict()
#     else:
#         models = mw.col.models.models
#     for line in lines:
#         id, model = oneLine(line)
#         models[str(id)]=model
#     mw.col.models.models = models
#     mw.col.models.changed = True
#     mw.col.models.flush()

def getRows():
    finder = Finder(mw.col)
    #all notes
    nids = finder.findNotes("")
    models = mw.col.models.models
    for nid in nids:
        note = mw.col.getNote(nid)
        mid = note.mid
        model = note._model
        if model is None:
            print(f"Note {nid}'s model {mid}({type(mid)}) is not a model.")
        modelName = model["name"]
        try:
            yield (
                note.id,
                note.guid,
                note.mod,
                modelName,
                note.usn
            )
        except:
            raise
table = Table(name, columns, getRows, allLines)
