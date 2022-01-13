from db import DB
from log import Log

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

log, dbTable = openLog('log.txt')

db = DB('localhost', 'bd2', 'teste', 'teste')

dbTableColumns = {}
dbTableData = {}
for line in dbTable:
    line = line.split('=')
    line[0] = line[0].split(',')
    dbTableColumns[line[0][0]] = 'integer'
    if dbTableData.get(line[0][1]) == None:
        dbTableData[line[0][1]] = {}
    dbTableData[line[0][1]][line[0][0]] = line[1]

db.createTable('log', dbTableColumns)
db.fillTable('log', dbTableData)

log = Log(log, db.tableColumns['log'])
log.parse()
log.showResults()