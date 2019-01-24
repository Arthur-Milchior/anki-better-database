from aqt import mw
from anki.db import DB
import os
path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name
db = DB(f"{path}/clearer.{name}.sqlite3")

class Data:
    def __init__(self,table, getRows, fromRows):
        self.table = table
        self.getRows = getRows
        self.fromRows = fromRows

    def clarify(self):
        self.table.execute(self.getRows)

    def reconstruct(self):
        pass
