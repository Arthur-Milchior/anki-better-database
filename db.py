from aqt import mw
from anki.db import DB
import os
path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name
db = DB(f"{path}/clearer.{name}.sqlite3")


class Reference:
    def __init__(self, table, column, delete = None, update = None):
        self.table = table
        self.column = column
        self.delete = delete
        self.update = update
        self.notNull = notNull
        self.primary = primary

    def create(self):
        t = f"references {self.table} ({self.column})"
        if self.delete:
            t+= f" on delete {self.delete}"
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

    def create(self):
        t = self.name
        if self.type:
            t += f" {self.type}"
        if self.unique:
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
    def __init__(self, name, columns, unique = None):
        self.name = name
        self.unique = unique
        self.columns = columns
        for i in range(len(columns)):
            column = columns[i]
            if isinstance(columns, str):
                columns[i] = Column(column)
        Table.tables.append(self)

    def create(self):
        t = "CREATE table if not exists {self.name} ("
        first = True
        for column in self.columns:
            if first:
                first = False
            else:
                t+=", "
            t+=column.create()
        if self.unique:
            t+= "UNIQUE ("
            first = True
            for unique in self.unique:
                if first:
                    first = False
                else:
                    t+=", "
                t+= unique
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
        for  column in self.columns:
            if first:
                first = False
            else:
                query+=", "
            query+=column.name
        query+=") values(?"
        query+=",?"*(len(self.columns)-1)
        query += ")"
        print(query)
        return query

    def insert(self,rows):
        try:
            db.executemany(self.insert_query(),rows)
        except:
            print(f"Rows are\n----------\n")
            for row in rows:
                print(row)
            print(f"\n--------------\n")
            raise

    def create(self):
        db.execute(self.create_query())

    def delete(self):
        db.execute(self.delete_query())

    def execute(self, rows):
        self.delete()
        self.create()
        self.insert(rows)
        db.commit()
