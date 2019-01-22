from aqt import mw
import .fieldnames
name= "fields"
column=[("nid", "INTEGER REFERENCES notes (id) ON DELETE CASCADE  ON UPDATE CASCADE"),
        ("name", "TEXT    REFERENCES fieldnames (name)"),
        ("value","TEXT")
]

end = """ UNIQUE (
        ord,
        nid
    )"""

def getRows():
    nids = mw.col.findNotes("")
    for nid in nids:
        note = mw.col.getNote(nid)
        mid = note.mid
        model = mw.col.models.get(mid)
        fieldNames = mw.col.models.fieldNames(model)
        for ord in len(note.fields):
            value = note.fields[ord]
            name = fieldNames[ord]
            yield (nid,name, value)
from meta import Data
Data(name, column, getRows,end)
