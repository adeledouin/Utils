# Notes DuckdbDriver : SQL & Python

## Liste dataframe query

L'idée est de noter ici les différentes fonction de fetch de donnée 
ainsi que la dataframe "cachée" à l'interieur la cas échéant 

auquel on ajoute la query SQL associée

### A ajouter/Updater gestion des stats 

```

        rel = db.fetch_stats(signal_table, column, batch_table=batch_table, b_idx=b_idx, where_clause=where_clause)
        db.insert_from_rel(batch.stat_table)
        query = f"""SELECT MEAN(rowid) AS meanrowid,
                            MIN({column}) AS min,
                            MAX({column}) AS max,
                            MEAN({column}) AS mean,
                            VARIANCE({column}) AS var,
                            STDDEV({column}) AS std,
                            COUNT({column}) AS count
                        FROM {signal_table}
                        WHERE {signal_table}.rowid >= (
                            SELECT start_id
                            FROM {batch_table}
                            WHERE rowid=0
                        ) AND {signal_table}.rowid <= (
                            SELECT end_id
                            FROM {batch_table}
                            WHERE rowid=0
                        ){where_clause_supp}
                        """
        bla = db.conv_to_pandas(db.sql(query))
        

```
### Signal mecha - force, position, acoustic
fetch all table signal
```
dataframe = db.fetch_signal(signal.table)

query = f"SELECT rowid, * FROM {signal.table}"
```

fetch specific rowid from table signal
```
idx = signal.subsample_idx(signal.N_pts_max, sample_rate=signal.acq_fr)
dataframe = db.fetch_from_idx(signal.table, idx)

query = f"SELECT rowid, * FROM {signal.table} WHERE rowid IN {idx}"
```

fetch from batch signal
```
start_id, end_id = db.fetch_batch_ids(batch.table, b=batch_idx)
dataframe = db.fetch_from_batch(signal.table, start_id, end_id)

query = f"""SELECT rowid, * FROM {signal.table} 
            WHERE rowid >= {start_id} AND rowid <= {end_id}"
```

fetch stats from all signal
```
db.fetch_stats(signal.table)
dataframe = self.fetch_signal(signal.table,
                              expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                              clause='')
                              
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
            FROM {signal.table}"""
```

fetch stats from idx signal
```
db.fetch_stats(signal.table)
dataframe = self.fetch_from_idx(signal.table,
                                idx=idx,
                                expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                                where_expr='rowid',
                                where_clause='')
                                
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
             FROM {signal.table}
             WHERE rowid IN {idx}""
```

fetch stats from batch signal
```
start_id, end_id = db.fetch_batch_ids(batch.table, b=batch_idx)
db.fetch_stats(signal.table, batch=[ini, end])
dataframe = self.fetch_from_batch(signal.table,
                                  start_id=batch[0], end_id=batch[-1],
                                  expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                                  clause_supp='')
                                
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
             FROM {signal.table}
             WHERE rowid >= {start_id} AND rowid <= {end_id}""
```
### Events start_id and end_id 

fetch all table idx
```
dataframe = db.fetch_signal(signal.idx_table)

query = f"SELECT rowid, * FROM {signal.idx_table}"
```

fetch specifics rowid from table idx => ici les idx correspondent à des numero d'events
```
idx = event n°N
dataframe = db.fetch_from_idx(signal.table, idx)
```

!!!! faudra coder fetch from idx correspondant à event avec condition sur event.quantité
=> a voir si nécéssaire ou pas...

fetch from batch table idx
```
start_id, end_id = db.fetch_batch_ids(batch.event_table, b=batch_idx)
dataframe = db.fetch_from_batch(signal.table, start_id, end_id)

query = f"""SELECT rowid, * FROM {signal.idx_table} 
            WHERE start_id >= {start_id} AND end_id <= {end_id}"
```

### Events index & number 
Si tous les éléments de event alors utiliser les mêmes commandes pour quel n'import quel signal

Si s'interesse uniquement aux éléments de event correspondants à des événements, soit où ``` number is not NULL```

fetch all table event
```
dataframe = db.fetch_signal(signal.event_table, clause=f" WHERE number IS NOT NULL")

query = f"SELECT rowid, * FROM {signal.event_table} WHERE number IS NOT NULL"
```

fetch from batch event
```
start_id, end_id = db.fetch_batch_ids(batch.event_table, b=batch_idx)
dataframe = db.fetch_from_batch(signal.event_table, start_id, end_id,
                                clause_supp=f" AND number IS NOT NULL")

query = f"""SELECT rowid, * FROM {signal.event_table} 
            WHERE rowid >= {start_id} AND rowid <= {end_id}
            AND number IS NOT NULL"""
```


Si s'interesse uniquement aux éléments de df correspondants à des événements PARTICULIERS, soit où ``` index IN list(idx)```

=> remplacer les ```WHERE number IS NOT NULL``` par ```WHERE index is IN {ist events}```

fetch from idx table event
```
dataframe = self.fetch_from_idx(signal.event_table, idx=idx, 
                                where_expr='index')

query = f"SELECT rowid, * FROM {signal.event_table} WHERE index IN {idx}"
```

fetch stats from idx table df
```
db.fetch_stats(signal.event_table, idx=idx, where_expr='index')
dataframe = self.fetch_signal(signal.event_table,
                              expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                              where_expr='index')
                              
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
            FROM {signal.event_table}
            WWHERE index IN {idx}"""
```

### Events Df & Dt
Si tous les éléments de df alors utiliser les mêmes commandes pour quel n'import quel signal

Si s'interesse uniquement aux éléments de df correspondants à des événements, soit où ``` number is not NULL```

fetch all table df
```
dataframe = db.fetch_signal(signal.df_table, clause=f" WHERE number IS NOT NULL")

query = f"SELECT rowid, * FROM {signal.df_table} WHERE number IS NOT NULL"
```

fetch from batch df
```
start_id, end_id = db.fetch_batch_ids(batch.df_table, b=batch_idx)
dataframe = db.fetch_from_batch(signal.df_table, start_id, end_id,
                                clause_supp=f" AND number IS NOT NULL")

query = f"""SELECT rowid, * FROM {signal.df_table} 
            WHERE rowid >= {start_id} AND rowid <= {end_id}
            AND number IS NOT NULL"""
```

fetch stats from all df
```
db.fetch_stats(signal.df_table, clause=f" WHERE number IS NOT NULL")
dataframe = self.fetch_signal(signal.df_table,
                              expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                              clause=f" WHERE number IS NOT NULL")
                              
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
            FROM {signal.df_table}
            WHERE number IS NOT NULL"""
```

fetch stats from batch df
```
start_id, end_id = db.fetch_batch_ids(batch.df_table, b=batch_idx)
db.fetch_stats(signal.df_table, batch=[ini, end], clause=f" AND number IS NOT NULL")
dataframe = self.fetch_from_batch(signal.df_table,
                                  start_id=batch[0], end_id=batch[-1],
                                  expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                                  clause_supp=f" AND number IS NOT NULL")
                                
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
             FROM {signal.df_table}
             WHERE rowid >= {start_id} AND rowid <= {end_id}
             AND number IS NOT NULL""
```

Si s'interesse uniquement aux éléments de df correspondants à des événements PARTICULIERS, soit où ``` index IN list(idx)```

=> remplacer les ```WHERE number IS NOT NULL``` par ```WHERE index is IN {ist events}```

fetch from idx table df
```
dataframe = self.fetch_from_idx(signal.df_table, idx=idx, 
                                where_expr='index')

query = f"SELECT rowid, * FROM {signal.df_table} WHERE index IN {idx}"
```

fetch stats from idx table df
```
db.fetch_stats(signal.df_table, idx=idx, where_expr='index')
dataframe = self.fetch_signal(signal.df_table,
                              expr=f"MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count",
                              where_expr='index')
                              
query = f"""SELECT MIN({column}) AS min, MAX({column}) AS max, MEAN({column}) AS mean, STDDEV({column}) AS std, COUNT({column}) as count 
            FROM {signal.df_table}
            WWHERE index IN {idx}"""
```
