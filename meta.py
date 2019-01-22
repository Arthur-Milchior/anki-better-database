from aqt import mw

class Data:
    tables = []
    def __init__(name, fields, getRows,end=""):
        self.name = name
        self.fields = fields
        for i in range(self.fields):
            if isinstance(self.field[i],str):
                self.field[i]=(self.field[i], "")
        self.getRows = getRows
        self.end = end
        Data.tables.append(self)

    def create_query():
        query = f"CREATE if not presents {self.name} decks ("
        first = True
        for column, param in self.fields:
            if first:
                first = False
            else:
                query+=", "
            query+=f"{column} {param}"
        query+=");"
        query+=self.end
        return query

    def insert_query():
        query = f"insert or replace into {self.name} ("
        first = True
        for  field,_ in self.fields:
            if first:
                first = False
            else:
                query+=", "
            query+=self.name
        query+=") values(?"
        query+=",?"*(len(self.fields)-1)
        query += ")"

    def create(self):
        mw.col.db.execute(self.create_query())

    def insert(self):
        mw.col.db.executemany(self.insert_query(),self.getRows())

    def execute(self):
        self.create()
        self.insert()
