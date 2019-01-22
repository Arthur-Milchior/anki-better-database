from .tables.configurations import *
from .tables.decks import *
from .tables.fieldnames import *
from .tables.fields import *
from .tables.models import *
from .tables.tags import *
from .tables.template import *

from .meta import Data


from aqt.qt import QAction

def run():
    for table in Data.tables:
        table.execute()



action = QAction(mw)
action.setText("Clarify the database")
mw.form.menuTools.addAction(action)
action.triggered.connect(run)
