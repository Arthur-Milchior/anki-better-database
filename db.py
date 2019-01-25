from aqt import mw
from anki.db import DB
import os
from .config import considerTable, getDb, isTableInSameDb
from .utils import *

path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name



class Reference:
    def __init__(self, table, column, delete = None, update = None):
        self.table = table
        self.column = column
        self.delete = delete
        self.update = update
        self.notNull = notNull
        self.primary = primary

    def create(self):
        if not considerTable(self.name):
            return ""
        t = f"references {self.table} ({self.column})"
        if self.delete:
            t+= f" on delete {self.delete}"
        if self.update:
            t+= f" on update {self.update}"
        return t

setNull = "set null"
cascade = "cascade"
class Column:
    def __init__(self, name, type = None, reference = None, uniques = None, primary = None, notNull = None):
        self.name = name
        self.type = type
        self.reference = reference
        self.uniques = uniques

    def create(self):
        t = self.name
        if self.type:
            t += f" {self.type}"
        if self.uniques:
            t += f" unique"
        if self.reference:
            t += f" "+reference.create()
        if self.primary:
            t+= f" primary key"
        if self.notNull:
            t+= f" Not null"
        return t

class Table:
    tables = []
    def __init__(self, name, columns, uniques = None, order = None):
        self.name = name
        self.uniques = uniques
        self.columns = columns
        if isinstance(order,type):
            order = [order]
        self.order = order
        order.solt = order
        for i in range(len(columns)):
            column = columns[i]
            if isinstance(columns, str):
                columns[i] = Column(column)
        Table.tables.append(self)

    def create(self):
        t = "CREATE table if not exists {self.name} ("
        t+=commaJoin(self.columns, lambda colum:column.create())
        if self.uniques:
            t+= "UNIQUE ("
            t+= commaJoin(self.uniques)
            t+=")"
        t+= ");"
        return t

    def delete_query(self):
        query = f"DROP table if exists {self.name}"
        print(query)
        return query

    def insert_query(self):
        query = f"insert or replace into {self.name} ("
        first = True
        query+= commaJoin(self.columns, (lambda column:column.name))
        query+=") values(?"
        query+=",?"*(len(self.columns)-1)
        query += ")"
        print(query)
        return query

    def insert(self,rows):
        try:
            getDb().executemany(self.insert_query(),rows)
        except:
            print(f"Rows are\n----------\n")
            for row in rows:
                print(row)
            print(f"\n--------------\n")
            raise

    def create(self):
        getDb().execute(self.create_query())

    def delete(self):
        getDb().execute(self.delete_query())

    def execute(self, rows, checkConf = True):
        if checkConf and not considerTable(self.name):
            return
        self.delete()
        self.create()
        self.insert(rows)
        getDb().commit()

    def select_query(self):
        t = "select ("
        first = True
        t+= commaJoin(self.columns, (lambda column:column.name))
        t+=f") from {self.name}"
        if self.order:
            t+= f " order by "
            t+= commaJoin(self.order)
        return t

    def select(self):
        return getDb().all(self.select_query())
