from .tables import configurations
from .tables import decks
from .tables import fieldnames
from .tables import fields
from .tables import models
from .tables import tags
from .tables import template
from aqt import mw
from aqt.utils import tooltip
from aqt.qt import QAction,QKeySequence

datas = [x.table for x in [configurations, decks, fieldnames, fields,
                           models, tags, template ] ]

def run(action):
    for data in datas:
        getattr(data,action)()
    tooltip(f"Ended {action}")



action = QAction(mw)
action.setText("Clarify the database")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: run("clarify"))
action.setShortcut(QKeySequence("Ctrl+Shift+C"))

action = QAction(mw)
action.setText("Rebuild the database")
mw.form.menuTools.addAction(action)
action.setShortcut(QKeySequence("Ctrl+Shift+R"))
action.triggered.connect(lambda: run("rebuild"))

action = QAction(mw)
action.setText("Delete the new tables")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: run("delete"))

action = QAction(mw)
action.setText("Empty readable tables")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: run("empty"))
