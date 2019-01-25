from aqt import mw
from ..db import *
from ..config import *

name= "tags"
columns = [
    Column(name="nid", type="integer", reference= Reference(table="notes", column="id", onDelete=cascade, update= cascade)),
    Column(name="tag", type="TEXT"),
]

def getRows():
    nids = mw.col.findNotes("")
    for nid in nids:
        note = mw.col.getNote(nid)
        tags = note.tags
        for tag in tags:
            yield (nid, tag)

lastNid = None
lastNote = None
listTag = []

def endGroup():
    lastNote.setTagsFromStr(" ".join(listTag))
    lastNote.flush()

def getNote(nid):
    global lastNid
    if nid != lastNid:
        endGroup()
        lastNid = nid
        lastNote = mw.col.getNote(nid)
        if shouldDelete():
            listTag = []
        else:
            listTag = lastNote.tags
    return lastNote

def oneLine(line):
    """Python error while loading note if the nid does not exists"""
    nid,tag = line
    getNote(nid)
    listTag.append(tag)

def allLines(lines):
    for line in lines:
        oneLine(line)
table = Table(name, columns, getRows, allLines, uniques = ["tag","nid"], order = ["nid"])
