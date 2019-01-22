from aqt import mw
from anki.db import DB
import os
path = os.path.dirname(os.path.abspath(__file__))
name = mw.pm.name
db = DB(f"{path}/clearer.{name}.sqlite3")

class Data:
    tables = []
    def __init__(self, name, fields, getRows,end=""):
        self.name = name
        self.fields = fields
        for i in range(len(self.fields)):
            field = self.fields[i]
            if isinstance(field,str):
                self.fields[i]=(field, "")
        self.getRows = getRows
        self.end = end
        Data.tables.append(self)

    def create_query(self):
        query = f"CREATE table if not EXISTS {self.name}  ("
        first = True
        for column, param in self.fields:
            if first:
                first = False
            else:
                query+=", "
            query+=f"{column} {param}"
        if self.end:
            query+=f", {self.end}"
        query += ");"
        print(query)
        return query

    def insert_query(self):
        query = f"insert or replace into {self.name} ("
        first = True
        for  field,_ in self.fields:
            if first:
                first = False
            else:
                query+=", "
            query+=field
        query+=") values(?"
        query+=",?"*(len(self.fields)-1)
        query += ")"
        print(query)
        return query

    def create(self):
        db.execute(self.create_query())

    def insert(self):
        rows = self.getRows()
        try:
            db.executemany(self.insert_query(),rows)
        except:
            print(f"Rows are\n----------\n")
            for row in rows:
                print(row)
            print(f"\n--------------\n")
            raise

    def execute(self):
        self.create()
        self.insert()
        db.commit()
