from aqt import mw
from ..db import *

name= "tags"
columns = [
    Column(name="nid", type="INTEGER", references= Reference(table="notes", column="id", delete=cascade, update= cascade)),
    Column(name="tag", type="TEXT"),
]
table = Table(name, columns, ["tag","nid"])

def getRows():
    nids = mw.col.findNotes("")
    for nid in nids:
        note = mw.col.getNote(nid)
        tags = note.tags
        for tag in tags:
            yield (nid, tag)
from ..meta import Data
data = Data(name, columns, getRows, end)
