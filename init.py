from .tables import configurations
from .tables import decks
from .tables import fieldnames
from .tables import fields
from .tables import models
from .tables import tags
from .tables import templates
from .tables import notes
from .tables import cards
from aqt import mw
from aqt.utils import tooltip
from aqt.qt import QAction,QKeySequence
from .config import considerTable

datas = [x.table for x in [configurations, decks, fieldnames, fields,
                           models, tags, templates, notes, cards ] ]

def run(actions):
    if isinstance(actions, str):
        actions = [actions]
    for action in actions:
        for data in datas:
            if considerTable(data.name):
                getattr(data,action)()
    tooltip(f"Ended {action}")



action = QAction(mw)
action.setText("Anki to Readable")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: run(["clarify"
                                      #,"view"
]))
action.setShortcut(QKeySequence("Ctrl+Shift+C"))


action = QAction(mw)
action.setText("Readable to anki")
mw.form.menuTools.addAction(action)
action.setShortcut(QKeySequence("Ctrl+Shift+R"))
action.triggered.connect(lambda: run(["rebuild"]+([] if keepTable() else ["delete"])))

action = QAction(mw)
action.setText("Delete Readable tables")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: run("delete"))

action = QAction(mw)
action.setText("Empty Readable tables")
mw.form.menuTools.addAction(action)
action.triggered.connect(lambda: run("empty"))
