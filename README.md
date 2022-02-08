# Trabalho prático - Log REDO

**Objetivo**: implementar o mecanismo de log Redo com checkpoint usando o SGBD.

---


## Arquivo de log

O programa aceita como entrada um arquivo de log com o formato usado no arquivo `logExample.txt`, sendo ele:

```
Tabela do banco

Log
```

A tabela do banco deve ser descrita com cada linha representando uma célula da tabela no formato: `Atributo,id=valor` sendo que o valor sempre será do tipo inteiro.

Já cada linha do log deve seguir o formato:  `<transação, “id da tupla”,”coluna”, “valor novo”>`. Os checkpoints são demarcados por um `<Start CKPT(transações)>` e um `<End CKPT>` e os commits tem a forma `<commit transação>`

## Execução

Antes de executar o programa é necessário criar um `.env` de acordo com o `.env.example` e configurá-lo com as configurações do postgres. Para executar o programa use:

```
python3 main.py nomeDoArquivoDeLog
```