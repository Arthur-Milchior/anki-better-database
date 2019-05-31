from ..db.db import *
from ..db.columns import *
from aqt import mw
import json
from anki.find import Finder
import sys

name= "cards"
columns=[
    Column(name="id", type="integer", primary=True),
    Column(name="nid",type="int", reference= Reference("notes", "id",  onDelete = cascade, update = cascade)),
    Column(name="deck",type="text", reference= Reference("decks", "name",  onDelete = cascade, update = cascade)),
    Column(name="template", type="text", reference= Reference("template", "name", update=cascade, onDelete = cascade )),
    Column(name="mod",type="int"),
    Column(name="usn",type="INT"),
    Column(name="type",type="INT"),
    Column(name="queue",type="INT"),
    Column(name="due",type="INT"),
    Column(name="ivl",type="INT"),
    Column(name="factor",type="INT"),
    Column(name="reps",type="int"),
    Column(name="lapses",type="int"),
    Column(name="odue",type="int"),
    Column(name="odid",type="int"),
]


def oneLine(line):
    id, nid, deckName, templateName, mod, usn, type, queue, due, ivl, factor, reps, lapses, odue, odid, ord, did = line
    oldModel = mw.col.models.get(id)
    templates = oldModel["tmpls"]
    fields = oldModel["flds"]
    did = mw.col.decks.byName(deckName)
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
    cids = finder.findCards("")
    for cid in cids:
        card = mw.col.getCard(cid)
        deck = mw.col.decks.get(card.did)
        deckName = deck["name"]
        note = card.note()
        model = note._model
        modelName = model["name"]
        try:
            template = model["tmpls"][card.ord]
        except IndexError:
            print(f"""Card {cid} has ord {card.ord} and model {modelName}, which have only {len(model["tmpls"])} cards.""",file=sys.stderr)
            continue
        templateName = template["name"]
        try:
            yield (
                card.id,
                card.nid,
                deckName,
                templateName,
                card.mod,
                card.usn,
                card.type,
                card.queue,
                card.due,
                card.ivl,
                card.factor,
                card.reps,
                card.lapses,
                card.odue,
                card.odid
            )
        except:
            raise
table = Table(name, columns, getRows, allLines, uniques = [["template","nid"]], equalities = ["notes.id = cards.nid", "decks.name = cards.deck", "templates.model = notes.model"], viewColumns = [("ord","templates.ord"),("did","decks.id")], joins = ["decks", "templates","notes"])
