import psycopg2

class DB:
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

    def createTable(self, tableName: str) -> None: 
        self.openConnection()
        cursor = self.connection.cursor()

        cursor.execute('DROP TABLE IF EXISTS '+tableName)
        cursor.execute('CREATE TABLE ' + tableName + ' (id SERIAL PRIMARY KEY, A integer, B integer)')
        self.connection.commit()

        self.closeConnection()
