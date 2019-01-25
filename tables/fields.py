from ..debug import *
from aqt import mw
from ..db import *
import sys
import os

name= "fields"
columns=[
    Column(name="nid", type="integer", reference= Reference(table="notes", column="id", onDelete=cascade, update= cascade)),
    Column(name="name", type="TEXT", reference= Reference(table= "fieldnames", column="name", onDelete= cascade, update= cascade)),
    Column(name="value",type="TEXT")
]



lastNid = None
lastNote = None
seenNames = None
def getModelFromNote(note):
    mid = note.mid
    model = mw.col.models.get(mid)
    if model is None:
        print(f"Note {note.id}'s model id is {mid}, which corresponds to no model", file = os.stderr)
    return model

def getMap(note):
    model = getModelFromNote(note)
    if model is None:
        return None
    map = mw.col.models.fieldMap(model)
    return map

def endGroup():
    global lastNid, lastNote, seenNames
    if lastNid is None:
        return
    map = getMap(lastNote)
    if map is None:
        print(f"This this note can't be saved", file = os.stderr)
        return
    if len(seenNames)< len(map):
        print(f"""The following fields are in the model {getModelFromNote(lastNote)["name"]}, but not used in it's note {lastNid}:""", file = sys.stderr)
        for key in map:
            if key not in seenNames:
                print(key, file = sys.stderr)
        debug(f"""Their previous value were kept.""", file = sys.stderr)
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
    model = getModelFromNote(note)
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
table = Table(name, columns, getRows, allLines, uniques = ["name","nid"], order = ["nid"])
