class Reference:
    def __init__(self, table, column, onDelete = None, update = None):
        self.table = table
        self.column = column
        self.onDelete = onDelete
        self.update = update

    def create_query(self):
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

