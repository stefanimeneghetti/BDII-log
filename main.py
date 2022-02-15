import os
import sys
from dotenv import load_dotenv
from db import DB
from log import Log

load_dotenv()

if (len(sys.argv) < 2):
    print("É necessário informar o nome do arquivo de log")
    exit(0)

TABLE_NAME = os.environ.get('TABLE_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def openLog(fileName: str) -> list:
    with open(fileName, 'r', encoding='utf-8') as file: 
        log = []
        dbTable = []
        isLog = False
        for line in file:
            if line.strip() == '':
                isLog = True
                continue
            if (isLog):
                log.append(line.strip())
            else:
                dbTable.append(line.strip())
        return log, dbTable

log, dbTable = openLog(sys.argv[1])

db = DB(DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

dbTableColumns = {}
dbTableData = {}
for line in dbTable:
    line = line.split('=')
    line[0] = line[0].split(',')
    dbTableColumns[line[0][0]] = 'integer'
    if dbTableData.get(line[0][1]) == None:
        dbTableData[line[0][1]] = {}
    dbTableData[line[0][1]][line[0][0]] = line[1]

db.createTable(TABLE_NAME, dbTableColumns)
db.fillTable(TABLE_NAME, dbTableData)

log = Log(log, db.tableColumns[TABLE_NAME], db)
log.parse()
log.executeREDO()
log.showResults()