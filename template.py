from aqt import mw
import .models
import .decks

name= "template"
fields = [
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


def getRow():
    models = mw.col.models.models
    for model in models:
        for template in model["tpmls"]:
            yield (
                model["mid"],
                model["ord"],
                model["afmt"],
                model["bafmt"],
                model["qfmt"],
                model["bqfmt"],
                model["did"],
                model["name"],
            )
from meta import Data
Data(name, fields, getRows)
