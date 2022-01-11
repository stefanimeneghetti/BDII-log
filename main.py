from db import DB

def openLog(fileName: str) -> list:
    with open(fileName, 'r', encoding='utf-8') as file: 
        log = []
        bdTable = []
        isLog = False
        for line in file:
            if line.strip() == '':
                isLog = True
                continue
            if (isLog):
                log.append(line.strip())
            else:
                bdTable.append(line.strip())
        return log, bdTable

log, bdTable = openLog('log.txt')

db = DB('localhost', 'bd2', 'teste', 'teste')
db.createTable('log')
