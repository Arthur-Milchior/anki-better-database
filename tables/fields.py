from aqt import mw
from .fieldnames import data
from ..db import *
import sys

name= "fields"
column=[
    Column(name="nid", type="INTEGER"#, reference= Reference(table="notes", column="id", delete=cascade, update= cascade)
    ),
    Column(name="name", type="TEXT", references= Reference(column= "fieldnames", column="name", delete= CASCADE, update= cascade)),
    Column(name="value",type="TEXT")
]

table = Table(name, columns, ["name","nid"], order = ["nid"])

lastNid = None
lastNote = None
seenNames = None
def getModel(note):
    mid = note.mid
    return mw.col.models.get(mid)

def getMap(note):
    model = getModel(note)
    map = mw.col.models.fieldMap(mid)
    return map

def endGroup():
    global lastNid, lastNote, seenNames
    if lastNid is None:
        return
    map = getMap(lastNote)
    if len(seenNames)< len(map):
        print(f"""The following fields are in the model {getModel(lastNote)["name"]}, but not used in it's note {lastNid}:""", file = sys.stderr)
        for key in map:
            if key not in seenNames:
                print(key, file = sys.stderr)
        print(f"""Their previous value were kept.""", file = sys.stderr)
        return
    lastNote.flush()

def getNote(nid):
    global lastNid, lastNote, seenNames
    if nid != lastNid:
        endGroup()
        lastNid = nid
        lastNote = mw.col.getNote(nid)
        seenNames = dict()
    return lastNote

def oneLine(line):
    """Python error while loading note if the nid does not exists"""
    nid,name,value = line
    note = getNote(nid)
    map = getMap(note)
    if name not in map:
        print (f"""You have a value for field {name} of note {nid} whose model is {model["name"]}, which does not have any field with this name""", file = sys.stderr)
        return
    seenNames[name] = value
    ord,_ = map.get(name)
    lastNote.fields[ord]=value
    return note

def allLines(lines):
    for line in lines:
        oneLine(line)
    endGroup()

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
data = Data(table, getRows, allLines)
