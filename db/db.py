from aqt import mw
from .columns import *
from ..config import getDb, isTableInSameDb
from ..utils import *
from ..config import *
from ..debug import *



class Table:
    def __init__(self, name, columns, getRows, rebuild, uniques = None, order = None, equalities=None, joins = None, viewColumns = None):
        self.name = name
        self.equalities = equalities
        self.joins = joins
        self.viewColumns = viewColumns
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

    def table_exists(self):
        return getDb().all("SELECT name FROM sqlite_master WHERE type='table' AND name='?';", self.name)

    def view_query(self):
        t= f"CREATE view "
        #t+=" if not exists "
        t+=f" full{self.name} ("
        t+=commaJoin(self.columns, (lambda column:column.name))
        t+=", "
        t+= commaJoin(self.viewColumns, (lambda x:x[0]))
        t+=") as select "
        t+=commaJoin(self.columns, (lambda column:f"{self.name}.{column.name}"))
        t+=", "
        t+=commaJoin(self.viewColumns, (lambda x:x[1]))
        t+=f" from {self.name} "
        for join in self.joins:
            t+= f" inner join {join} "
        t+=" on "
        t+=" and ".join(self.equalities)
        t+=";"
        print(t)
        return t

    def view(self):
        if self.viewColumns:
            getDb().execute(self.view_query())
            
        
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
        if self.table_exists():
            for query in self.empty_queries():
                getDb().execute(query)

    def clarify(self):
        self.delete()
        self.create()
        self.insert(self.getRows())
        getDb().commit()

    def select_all_query(self, condition=""):
        t = "select "
        first = True
        t+= commaJoin(self.columns, (lambda column:column.name))
        if self.viewColumns:
            t+=", "
            t+=commaJoin(self.viewColumns, (lambda x:x[0]))
        t+=" from "
        if self.joins:
            t+=f"full_{self.name}"
        else:
            t+=self.name
        if self.order:
            t+= " order by "
            t+= commaJoin(self.order)
        t+= condition
        t+=" ;"
        debug(t)
        return t

    def select(self,condition="", *args,**kwargs):
        query = self.select_all_query(condition, *args,**kwargs)
        return getDb().all(query)

    def scalar(self, column, condition= "", *args,**kwargs):
        query = f"Select {column} from {self.name} {condition}"
        return getDb().scalar(query, *args,**kwargs)
                
    def first(self, condition= "", *args,**kwargs):
        query = self.select_all_query(condition, *args,**kwargs)
        return getDb().first(query, *args,**kwargs)
                

