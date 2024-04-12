# A installer

- pip install duckdb

# create database

```
import duckdb

# create a connection to a file called 'duckdb_database.db'
con = duckdb.connect('duckdb_database.db')
# create a table and load data into it
con.sql('CREATE TABLE test(i INTEGER)')
con.sql('INSERT INTO test VALUES (42)')
# query the table
con.table('test').show()
# explicitly close the connection
con.close()
# Note: connections also closed implicitly when they go out of scope
```
# Data Input

## from initial row file
```
import duckdb
# specify options on how the CSV is formatted internally
duckdb.read_csv('example.csv', header=False, sep=',')
# use the (experimental) parallel CSV reader
duckdb.read_csv('example.csv', header=False, sep=',', parallel=True)
```

## from tranform csv file

- `cat force_1_Exp230526.txt | tr ',' '\n' > force_1_Exp230526_nocomma.txt` la commande a duré 167.36 secondes
- `dos2unix force_1_Exp230526_nocomma.txt` -> conversion des carriage return.

```
import duckdb
# read from a file using fully auto-detected settings
duckdb.read_csv('example.csv')
# read multiple CSV files from a folder
duckdb.read_csv('folder/*.csv')
# use the (experimental) parallel CSV reader
duckdb.read_csv('example.csv', parallel=True)
```

## with SQL from tranform csv file
```
# directly read a CSV file from within SQL
duckdb.sql("SELECT * FROM 'example.csv'")
# call read_csv from within SQL
duckdb.sql("SELECT * FROM read_csv_auto('example.csv')")
```