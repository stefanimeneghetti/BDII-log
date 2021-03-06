from db import DB
import os

class Log:
    transactions = []
    commitedTransactions = []
    validCheckpoint = False
    findEndCheckpoint = False
    findStartCheckpoint = False
    transactionChanges = {}
    outstandingTransactions = []
    findStart = []
    findTransactionStart = 0

    def __init__(self, log: list, tableColumns: list, db: DB) -> None:
        self.tableColumns = tableColumns
        self.db = db
        self.tableName = os.environ.get('TABLE_NAME')
        self.log = log[::-1]

    def parse(self) -> None:
        for line in self.log:
            line = line[1:].replace('>', '').lower()
            
            if line.startswith('commit'):
                self.commitedTransactions.append(line.split()[1])
            elif line.startswith('start') and 'ckpt' not in line and not self.findStartCheckpoint:
                self.transactions.append(line.split()[1])
                if line.split()[1] in self.findStart:
                    self.findTransactionStart += 1
            elif line.startswith('start') and self.findEndCheckpoint:
                if self.validCheckpoint and 'ckpt' in line:
                    self.findStartCheckpoint = True
                    self.outstandingTransactions = [x.strip() for x in line[line.index('(') + 1:line.index(')')].split(',')]
                    self.transactions += self.outstandingTransactions

                    for i in range (len(self.outstandingTransactions)):
                        if self.outstandingTransactions[i] in self.commitedTransactions:
                            self.findStart.append(self.outstandingTransactions[i])
                elif 'ckpt' not in line:
                    if line.split()[1] in self.findStart:
                        self.findTransactionStart += 1
                self.validCheckpoint = False
            elif line == 'end ckpt':
                if self.findEndCheckpoint == False:
                    self.findEndCheckpoint = True  
                    self.validCheckpoint = True
            elif not (line.startswith('start') and not self.findEndCheckpoint) and 'crash' not in line:
                operations = line.split(',')
                if self.transactionChanges.get(operations[0]) == None:
                    self.transactionChanges[operations[0]] = {}
                if self.transactionChanges[operations[0]].get(operations[1]) == None:
                    self.transactionChanges[operations[0]][operations[1]] = {}
                if self.transactionChanges[operations[0]][operations[1]].get(operations[2]) == None:
                    self.transactionChanges[operations[0]][operations[1]][operations[2]] = operations[3]
                           
            if (self.findStartCheckpoint) and self.findTransactionStart == len(self.findStart): # terminou de ler a parte necessaria do log
                break

    def showResults(self) -> None:
        print("Sa??da:\n")

        for transaction in self.transactions:
            if transaction in self.commitedTransactions:
                print(f"A transi????o {transaction} realizou REDO")
            elif transaction in self.outstandingTransactions:
                print(f"A transi????o {transaction} n??o realizou REDO")
        
        self.showVariables()

    def executeREDO(self) -> None:
        for transaction in reversed(self.commitedTransactions):
            if transaction in self.transactions:
                self.db.updateTable(self.tableName, self.transactionChanges[transaction])

    def showVariables(self):
        dbTable = self.db.selectTable(self.tableName)
        dbColumns = self.db.tableColumns[self.tableName]

        print("\nVari??veis:\n")

        for reg in dbTable:
            for index,column in enumerate(dbColumns):
                print(f"{reg[0]},{column} = {reg[index+1]}")