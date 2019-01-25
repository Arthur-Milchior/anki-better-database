from aqt import mw
from anki.db import DB
from .config import *
import os
path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name

class Data:
    def __init__(self,table, getRows, rebuild):
        self.table = table
        self.getRows = getRows
        self.rebuildFun = rebuild

    def clarify(self):
        self.table.execute(self.getRows)

    def rebuild(self):
        self.rebuildFun(self.table.select())
        if not keepTable():
            self.table.delete()
