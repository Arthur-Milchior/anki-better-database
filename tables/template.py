from aqt import mw
from .models  import data
from .decks import data
import sys
import json

name= "template"
fields = [
    ("json", "TEXT"),
    ("mid","INTEGER REFERENCES models (id) ON DELETE CASCADE"),
    ("ord","int"),
    ("afmt","Text"),
    ("bafmt","Text"),
    ("qfmt","Text"),
    ("bqfmt","Text"),
    ("did","INTEGER REFERENCES decks (id) ON DELETE SET NULL "),
    ("name","Text"),
]
end = """ UNIQUE (
        ord,
        mid
    )"""


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
