from ..db import *
from aqt import mw
from .models  import data
from .decks import data
import sys
import json

name= "template"
columns = [
    Column(name="json", type="TEXT"),
    Column(name="mid",type="INTEGER", reference= Reference("models", "id",  delete = cascade)),
    Column(name="ord",type="int"),
    Column(name="afmt",type="Text"),
    Column(name="bafmt",type="Text"),
    Column(name="qfmt",type="Text"),
    Column(name="bqfmt",type="Text"),
    Column(name="did",type="INTEGER", reference= Reference("models", "id",  delete = setNull)),
    Column(name="name",type="Text"),
]
table = Table(name, columns, ["ord","mid"])

def oneLine(line):
    json, mid, ord, afmt, bafmt, qfmt, bqfmt, did, name = line


def getRows():
    models = mw.col.models.models
    for model in models.values():
        mid = model["id"]
        if "tmpls" in model:
            for template in model["tmpls"]:
                yield (
                    json.dumps(template),
                    mid,
                    template["ord"],
                    template["afmt"],
                    template["bafmt"],
                    template["qfmt"],
                    template["bqfmt"],
                    template["did"],
                    template["name"],
                )
        else:
            print(f"No tmpls in {model}", file = sys.stderr)

from ..meta import Data
data = Data(name, fields, getRows)
