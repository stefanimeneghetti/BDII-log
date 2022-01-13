class Log:
    transactions = []
    commitedTransactions = []
    validCheckpoint = False
    lastCheckpoint = False
    findCheckpoint = False
    transactionChanges = {}
    outstandingTransactions = []
    findTransactionStart = 0

    def __init__(self, log: list, tableColumns: list) -> None:
        self.tableColumns = tableColumns
        self.log = log[::-1]

    def parse(self) -> None:
        for line in self.log:
            line = line[1:].replace('>', '').lower()

            if line.startswith('commit'):
                self.commitedTransactions.append(line.split()[1])
            elif line.startswith('start') and 'checkpoint' not in line:
                self.transactions.append(line.split()[1])
                if line.split()[1] in self.outstandingTransactions:
                    self.findTransactionStart += 1
            elif line.startswith('start') and self.lastCheckpoint:
                if (self.validCheckpoint):
                    self.findCheckpoint = True
                    self.outstandingTransactions = [x.strip() for x in line[line.index('(') + 1:line.index(')')].split(',')]
                self.validCheckpoint = False
            elif line == 'end checkpoint':
                if self.lastCheckpoint == False:
                    self.lastCheckpoint = True  
                    self.validCheckpoint = True
            else:
                operations = line.split(',')
                if self.transactionChanges.get(operations[0]) == None:
                    self.transactionChanges[operations[0]] = {}
                if self.transactionChanges[operations[0]].get(operations[1]) == None:
                    self.transactionChanges[operations[0]][operations[1]] = {}
                if self.transactionChanges[operations[0]][operations[1]].get(operations[2]) == None:
                    self.transactionChanges[operations[0]][operations[1]][operations[2]] = operations[3]
                           
            if (self.findCheckpoint) and self.findTransactionStart == len(self.outstandingTransactions): # terminou de ler a parte necessaria do log
                break

    def showResults(self) -> None:
        for transaction in self.transactions:
            if transaction in self.commitedTransactions:
                print(f"A transição {transaction} realizou REDO")
            elif transaction in self.outstandingTransactions:
                print(f"A transição {transaction} não realizou REDO")