import psycopg2

class DB:
    tableColumns = {}

    def __init__(self, host:str, database:str, user:str, password:str) -> None:
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    
    def openConnection(self) -> None:
        self.connection = psycopg2.connect(
            host = self.host, 
            database = self.database,
            user = self.user, 
            password = self.password
        )

    def closeConnection(self) -> None:
        self.connection.close()

    def createTable(self, tableName: str, columns:dict) -> None: 
        self.openConnection()
        cursor = self.connection.cursor()

        sql = 'CREATE TABLE ' + tableName + ' (id integer PRIMARY KEY'

        if self.tableColumns.get(tableName) == None:
            self.tableColumns[tableName] = []

        for column in columns:
            sql += ', ' + column + ' ' + columns[column]
            if column not in self.tableColumns[tableName]:
                self.tableColumns[tableName].append(column)
        
        sql += ')'

        cursor.execute('DROP TABLE IF EXISTS '+tableName)
        cursor.execute(sql)
        self.connection.commit()

        self.closeConnection()

    def fillTable(self, tableName, tableData: dict) -> None:
        self.openConnection()
        cursor = self.connection.cursor()
        tableColumns = self.tableColumns[tableName]
        columns = ''
        
        for item in tableColumns:
            columns += ', ' + item

        baseSql = 'INSERT INTO log (id' + columns + ') values ('

        for id in tableData:
            sql = baseSql + id
            for column in tableColumns:
                sql += ', ' + tableData[id][column]
            sql += ')'
            cursor.execute(sql)

        self.connection.commit()
        self.closeConnection()
