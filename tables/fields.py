from ..db.db import *
from ..db.columns import *
from ..debug import *
from aqt import mw
import sys
import os

name= "fields"
columns=[
    Column(name="nid", type="integer", reference= Reference(table="notes", column="id", onDelete=cascade, update= cascade)),
    Column(name="name", type="TEXT", reference= Reference(table= "fieldnames", column="name", onDelete= cascade, update= cascade)),
    Column(name="value",type="TEXT")
]


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

def endGroup(nid,note,seenNames):
    if note is None:
        return
    map = getMap(note)
    if map is None:
        print(f"This this note can't be saved", file = os.stderr)
        return
    if len(seenNames)< len(map):
        print(f"""The following fields are in the model {getModelFromNote(note)["name"]}, but not used in it's note {nid}:""", file = sys.stderr)
        for key in map:
            if key not in seenNames:
                print(key, file = sys.stderr)
        debug(f"""Their previous value were kept.""", file = sys.stderr)
        return
    note.flush()

def oneLine(line, lastNid, note, seenNames):
    """Python error while loading note if the nid does not exists"""
    nid,name,value = line
    if nid != lastNid:
        note = mw.col.getNote(nid)
        seenNames = dict()
    model = getModelFromNote(note)
    map = getMap(note)
    if name not in map:
        print (f"""You have a value for field {name} of note {nid} whose model is {model["name"]}, which does not have any field with this name""", file = sys.stderr)
        return
    seenNames[name] = value
    ord,_ = map.get(name)
    note.fields[ord]=value
    return nid,note,seenNames

def allLines(lines):
    nid = None
    note = None
    seenNames = dict()
    for line in lines:
        nid,note,seenNames = oneLine(line, nid, note, seenNames)
    endGroup(nid,note,seenNames)

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

def getField(nid,name):
    return table.scalar("value", " where name = ? and nid = ?", name,nid, equalities = ["fields.name = fieldnames.name", "notes.model = fieldnames.model"], viewColumns = [("ord","fieldnames.ord")], joins = ["fieldnames", "notes"])
