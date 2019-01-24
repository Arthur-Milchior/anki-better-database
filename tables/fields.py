from aqt import mw
from .fieldnames import data
from ..db import *

name= "fields"
column=[
    Column(name="nid", type="INTEGER"#, reference= Reference(table="notes", column="id", delete=cascade, update= cascade)
    ),
    Column(name="name", type="TEXT", references= Reference(column= "fieldnames", column="name", delete= CASCADE, update= cascade)),
    Column(name="value",type="TEXT")
]

table = Table(name, columns, ["name","nid"])
# def oneLine(line):
#     nid, name, value = line
#     return dict(
#         name = name,
#         value = value),nid


def getRows():
    nids = mw.col.findNotes("")
    for nid in nids:
        note = mw.col.getNote(nid)
        mid = note.mid
        model = mw.col.models.get(mid)
        fieldNames = mw.col.models.fieldNames(model)
        for ord in range(len(note.fields)):
            value = note.fields[ord]
            name = fieldNames[ord]
            yield (nid,name, value)
from ..meta import Data
data = Data(name, column, getRows,end)
