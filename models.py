from aqt import mw
import .decks
name= "models"
column=[
    ("css","Text"),
   ("did","INTEGER REFERENCES decks (id) ON DELETE SET NULL"),
   ("id","INTEGER UNIQUE PRIMARY KEY"),
   ("latexPost","Text"),
   ("latexPre","Text"),
   ("mod","int"),
   ("name","Text"),
   "req",
   ("sortf","int"),
   "tags",
   "tmpls"
   ("cloze","BOOLEAN"),
   ("usn","INT"),
   "vers",
]


def getRow():
    models = mw.col.models.models
    for model in models:
        yield (
            model["css"],
            model["did"],
            model["id"],
            model["latexPost"],
            model["latexPre"],
            model["mod"],
            model["name"],
            model["req"],
            model["sortf"],
            model["tags"],
            model["tmpls"],
            int(model["cloze"])==1,
            model["usn"],
            model["vers"]
            )
from meta import Data
Data(name, column, getRows)
