from aqt import mw
from .fieldnames import data

name= "fields"
column=[("nid", "INTEGER REFERENCES notes (id) ON DELETE CASCADE  ON UPDATE CASCADE"),
        ("name", "TEXT    REFERENCES fieldnames (name)"),
        ("value","TEXT")
]

end = """ UNIQUE (
        name,
        nid
    )"""

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
