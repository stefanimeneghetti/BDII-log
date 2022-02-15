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

        baseSql = 'INSERT INTO ' + tableName + ' (id' + columns + ') values ('

        for id in tableData:
            sql = baseSql + id
            for column in tableColumns:
                sql += ', ' + tableData[id][column]
            sql += ')'
            cursor.execute(sql)

        self.connection.commit()
        self.closeConnection()

    def updateTable(self, tableName: str, transactionData: dict) -> None:
        self.openConnection()
        cursor = self.connection.cursor()

        baseSql = 'UPDATE ' + tableName + ' SET '

        for id in transactionData:
            sql = ''
            for column in transactionData[id]:
                if sql != '':
                    sql += ', '
                sql += column + '=' + transactionData[id][column]
            sql = baseSql + sql + ' WHERE id = ' + id
            cursor.execute(sql)        

        self.connection.commit()
        self.closeConnection()

    def selectTable(self, tableName: str) -> list:
        self.openConnection()
        cursor = self.connection.cursor()
        columns = 'id'
        for column in self.tableColumns[tableName]:
            columns += ', ' + column
        cursor.execute('SELECT ' + columns + ' FROM '+tableName+';')
        res = cursor.fetchall()
        self.closeConnection()

        return res
