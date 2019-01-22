from aqt import mw

name= "fields"
l=[("nid", "INTEGER REFERENCES notes (id) ON DELETE CASCADE  ON UPDATE CASCADE"),
   ("tag", "TEXT"),
]
end = """ UNIQUE (
        tag,
        nid
    )"""

def getRow():
    nids = mw.col.findNotes("")
    for nid in nids:
        note = mw.col.getNote(nid)
        tags = note.tags
        for tag in tags:
            yield (nid, tag)
from meta import Data
Data(name, fields, getRows,end)
