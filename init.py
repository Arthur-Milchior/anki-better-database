import configurations
import decks
import fieldnames
import fields
import models
import tags
import template
from meta import Data

from aqt.qt import QAction

def run():
    for table in Data.tables:
        table.execute



action = QAction(mw)
action.setText("Clarify the database")
mw.form.menuTools.addAction(action)
action.triggered.connect(run)
