from aqt import mw
from .config import considerTable, getDb, isTableInSameDb
from .utils import *
from .config import *
from .debug import *



class Reference:
    def __init__(self, table, column, onDelete = None, update = None):
        self.table = table
        self.column = column
        self.onDelete = onDelete
        self.update = update

    def create_query(self):
        if not considerTable(self.table):
            return ""
        t = f"references {self.table} ({self.column})"
        if self.onDelete:
            t+= f" on Delete {self.onDelete}"
        if self.update:
            t+= f" on update {self.update}"
        return t

setNull = "set null"
cascade = "cascade"
class Column:
    def __init__(self, name, type = None, reference = None, unique = None, primary = None, notNull = None):
        self.name = name
        self.type = type
        self.reference = reference
        self.unique = unique
        self.notNull = notNull
        self.primary = primary

    def create_query(self):
        t = self.name
        if self.type:
            t += f" {self.type}"
        if self.unique:
            t += f" unique"
        if self.reference:
            t += f" "+self.reference.create_query()
        if self.primary:
            t+= f" primary key"
        if self.notNull:
            t+= f" Not null"
        return t

class Table:
    def __init__(self, name, columns, getRows, rebuild, uniques = None, order = None):
        self.name = name
        if uniques and isinstance(uniques[0], str):
            uniques = [uniques]
        self.uniques = uniques
        self.columns = columns
        if isinstance(order,type):
            order = [order]
        self.order = order
        self.getRows = getRows
        self.rebuildFun = rebuild
        for i in range(len(columns)):
            column = columns[i]
            if isinstance(column, str):
                columns[i] = Column(column)

    def rebuild(self):
        self.rebuildFun(self.select())
        if not keepTable():
            self.delete()


    def create_query(self):
        t = f"CREATE table if not exists {self.name} ("
        t+=commaJoin(self.columns, (lambda column:column.create_query()))
        if self.uniques:
            for uniques in self.uniques:
                t+= ", UNIQUE ("
                t+= commaJoin(uniques)
                t+=")"
        t+= ");"
        debug(t)
        return t

    def delete_query(self):
        query = f"DROP table if exists {self.name};"
        debug(query)
        return query

    def empty_queries(self):
        queries = [f"delete from {self.name};"]
        debug(queries)
        return queries

    def insert_query(self):
        query = f"insert or replace into {self.name} ("
        first = True
        query+= commaJoin(self.columns, (lambda column:column.name))
        query+=") values(?"
        query+=",?"*(len(self.columns)-1)
        query += ")"
        debug(query)
        return query

    def insert(self,rows):
        try:
            getDb().executemany(self.insert_query(),rows)
        except:
            debug(f"Rows are\n----------\n")
            for row in rows:
                debug(row)
            debug(f"\n--------------\n")
            raise

    def create(self):
        getDb().execute(self.create_query())

    def delete(self):
        getDb().execute(self.delete_query())

    def empty(self):
        for query in self.empty_queries():
            getDb().execute(query)

    def clarify(self):
        if not considerTable(self.name):
            return
        self.delete()
        self.create()
        self.insert(self.getRows())
        getDb().commit()

    def select_query(self):
        t = "select "
        first = True
        t+= commaJoin(self.columns, (lambda column:column.name))
        t+=f" from {self.name}"
        if self.order:
            t+= " order by "
            t+= commaJoin(self.order)
        t+=" ;"
        debug(t)
        return t

    def select(self):
        return getDb().all(self.select_query())
