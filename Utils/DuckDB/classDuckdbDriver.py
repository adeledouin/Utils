import duckdb
import logging
import timeit
import pandas as pd
import polars

import numpy as np
from Data.dict_data_str import *


def value_chaine(chaine):
    logging.debug('{}'.format(chaine))
    count = 0
    for astep in np.asarray(list(summary_value_astep.keys())):
        if astep in chaine:
            logging.debug('astep {} in chaine so + {}'.format(astep, summary_value_astep[astep]))
            count = count + summary_value_astep[astep]
    for signaltype in np.asarray(list(summary_value_signaltype.keys())):
        if signaltype in chaine:
            logging.debug('signaltype {} in chaine'.format(signaltype))
            count = count + summary_value_signaltype[signaltype]
    for eventtype in np.asarray(list(summary_value_eventtype.keys())):
        if eventtype in chaine:
            logging.debug('eventtype {} in chaine'.format(eventtype))
            count = count + summary_value_eventtype[eventtype]
    logging.debug('chaine {} count {}'.format(chaine, count))
    return count


# ------------------------------------------
class DuckDBDriver():
    # ---------------------------------------------------------#
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.con = None

    # ---------------------------------------------------------#
    # -------------- database standart commands ---------------#
    # ---------------------------------------------------------#
    def connect_database(self, progress=True) -> None:
        logging.warning("connecting to {}".format(self.db_path))
        con = duckdb.connect(self.db_path)
        if progress:
            con.execute("PRAGMA enable_progress_bar")
        con.execute("SET memory_limit = '20GB'")
        logging.debug("Executed PRAGMA commands")
        self.con = con

    # ---------------------------------------------------------#
    def connect_memory_db(self, progress=True):
        con = duckdb.connect(":memory:")
        if progress:
            con.execute("PRAGMA enable_progress_bar")
        con.execute("SET memory_limit = '20GB'")
        logging.debug("Executed PRAGMA commands")
        self.con = con

    # ---------------------------------------------------------#
    def close_con(self) -> None:
        logging.info("closing connection....")
        if self.con is not None:
            self.con.close()

    # ---------------------------------------------------------#
    def execute(self, query: str) -> None:
        logging.debug(f"executing {query}")
        start_time = timeit.default_timer()
        self.con.execute(query)
        stop_time = timeit.default_timer()
        logging.debug("query took {}".format(stop_time - start_time))

    # ---------------------------------------------------------#
    def sql(self, query: str) -> duckdb.DuckDBPyRelation:
        logging.debug(f"executing {query}")
        start_time = timeit.default_timer()
        con_sql = self.con.sql(query)
        stop_time = timeit.default_timer()
        logging.debug("query took {}".format(stop_time - start_time))

        return con_sql

    # ---------------------------------------------------------#
    # --------------- database tables commands ----------------#
    # ---------------------------------------------------------#
    def create_table(self, table_to_create: str, column_info='val INT2', reset_table=True) -> None:
        """ create tables in the duckdb database"""
        if reset_table:
            self.drop_table(table_to_create)
        logging.debug("Creating tables in {}".format(self.db_path))
        query = f"CREATE TABLE {table_to_create} ({column_info})"
        try:
            # create table one by one
            self.execute(query)
        except (Exception, duckdb.CatalogException) as error:
            print(error)

    # ---------------------------------------------------------#
    def create_table_from_dataframe(self, table_to_create: str, dataframe: str, reset_table=True) -> None:
        """ create tables in the duckdb database"""
        if reset_table:
            self.drop_table(table_to_create)
        logging.debug("Creating table in {} from numpy array".format(self.db_path))
        query = f"CREATE TABLE {table_to_create} AS SELECT * FROM {dataframe}"
        try:
            # create table one by one
            self.execute(query)
        except (Exception, duckdb.CatalogException) as error:
            print(error)

    # ---------------------------------------------------------#
    def create_table_from_rel(self, table_to_create: str, reset_table=True) -> None:
        """ create tables in the duckdb database"""
        if reset_table:
            self.drop_table(table_to_create)
        logging.debug("Creating table in {} from numpy array".format(self.db_path))
        query = f"CREATE TABLE {table_to_create} AS SELECT * FROM {'rel'}"
        try:
            # create table one by one
            self.execute(query)
        except (Exception, duckdb.CatalogException) as error:
            print(error)

    # ---------------------------------------------------------#
    def alter_table(self, table_name: str, column_name: str, data_type: str) -> None:
        alter_query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};"
        logging.debug(f"alter_table query {alter_query}")
        # Connexion à la base de données
        try:
            # Requête pour alterer les tables de la base de données : add colone
            self.execute(alter_query)
        except (Exception, duckdb.CatalogException) as error:
            print(error)

    # ---------------------------------------------------------#
    def drop_table(self, table_name: str) -> None:
        logging.debug(f"Deleting table {table_name} if it exists")
        drop_query = f"DROP TABLE IF EXISTS {table_name}"
        logging.debug(f"drop_table query {drop_query}")
        try:
            # Requête pour alterer les tables de la base de données : add colone
            self.execute(drop_query)
        except (Exception, duckdb.CatalogException) as error:
            print(error)

    # ---------------------------------------------------------#
    def summary_database(self) -> None:
        """print summary database"""
        # Requête pour récupérer les noms des tables de la base de données
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables_result = self.con.execute(tables_query)
        tables = [row[0] for row in tables_result.fetchall()]

        # Trier la liste en utilisant la fonction de tri personnalisée
        tables = sorted(tables, key=value_chaine)

        # Affichage de la structure pour chaque table
        for table in tables:
            describe_query = f"SELECT * FROM {table} LIMIT 1;"
            describe_result = self.con.execute(describe_query)

            # Récupération des noms des colonnes à partir du résultat
            column_names = [column[0] for column in describe_result.description]
            data_types = [column[1] for column in describe_result.description]
            count_line = self.count_row(table)
            print(f"Table '{table}': column - {column_names} | count {count_line}")
            print("=" * 30)

    # ---------------------------------------------------------#
    # ------------------ database INSERT ----------------------#
    # ---------------------------------------------------------#
    def insert_val(self, table_name: str, column_name: str, val: float) -> None:
        logging.debug("todo")
        query = f"INSERT INTO {table_name} ({column_name}) VALUES ({val})"
        self.execute(query)

    # ---------------------------------------------------------#
    def insert_from_csv(self, table_name: str, column_name: str, csv_path: str) -> None:
        logging.debug("todo")
        query = f"INSERT INTO {table_name} ({column_name}) SELECT column0 FROM read_csv_auto('{csv_path}')"
        self.execute(query)

    # ---------------------------------------------------------#
    def insert_from_dataframe(self, table_name: str, dataframe, expr: str = '*', column_name: str = None) -> None:
        logging.debug("todo")
        if column_name is None:
            query = f"INSERT INTO {table_name} SELECT * FROM {dataframe}"
        else:
            query = f"INSERT INTO {table_name} ({column_name}) SELECT {expr} FROM {dataframe}"
        self.execute(query)

    # ---------------------------------------------------------#
    def insert_from_rel(self, table_name: str, column_name: str = None, expr: str = '*') -> None:
        logging.debug("todo")
        if column_name is None:
            query = f"INSERT INTO {table_name}  SELECT * FROM {'rel'}"
        else:
            query = f"INSERT INTO {table_name} ({column_name}) SELECT {expr} FROM {'rel'}"
        self.execute(query)

    # ---------------------------------------------------------#
    # ------------------ database UPDATE ----------------------#
    # ---------------------------------------------------------#
    def update_in_batch_from_table(self, new_table_name: str, new_column_name: str, old_table_name: str,
                                   old_column_name: str, batch_size: int = 100000000) -> None:
        logging.debug("todo")

        nb_rows = self.count_raw(old_table_name)
        # Parcourez les lots et effectuez les mises à jour par lot
        for i in range(0, nb_rows, batch_size):
            logging.debug("batch {}".format(i))
            start_rowid = i
            end_rowid = min(i + batch_size, nb_rows)
            print(start_rowid, end_rowid)

            query = f"""
                    UPDATE {new_table_name} SET {new_column_name}=(SELECT {old_column_name} FROM {old_table_name} 
                    WHERE {new_table_name}.rowid = {old_table_name}.rowid 
                    AND {old_table_name}.rowid BETWEEN {start_rowid} AND {end_rowid})
                    WHERE {new_table_name}.rowid BETWEEN {start_rowid} AND {end_rowid}
                    """
            self.execute(query)

    # ---------------------------------------------------------#
    def update_in_batch_from_csv(self, table_name: str, column_name: str, csv_path: str) -> None:
        logging.debug("todo")
        logging.debug("deleting table tmp if it exists")
        self.con.execute("DROP TABLE IF EXISTS tmp")
        self.con.execute("CREATE TABLE tmp (val INT2)")
        self.insert_from_csv('tmp', 'val', csv_path)
        self.update_in_batch_from_table(table_name, column_name, 'tmp', 'val')

    # ---------------------------------------------------------#
    # ----------- database CLAUSE/JOIN queries ----------------#
    # ---------------------------------------------------------#
    def conv_numpy_to_IN_clause(self, array) -> str:
        return f" IN ({','.join(map(str, array))})"

    # ---------------------------------------------------------#
    def conv_pandas_to_IN_clause(self, df, column_name) -> str:
        ''' à utiliser dans clause de ex : clause = f" WHERE rowid{clause}"
        query = f"SELECT rowid, * FROM {table_name}{clause};"'''
        # Convertir la colonne idxs en une liste Python
        idxs_list = df[column_name].tolist()
        return self.conv_numpy_to_IN_clause(idxs_list)

    # ---------------------------------------------------------#
    def USING_random_idx_nb_clause(self, nb_raw: int) -> str:
        ''' à utiliser dans clause de ex : query = f"SELECT rowid, * FROM {table_name}{clause};"'''
        # -- select a sample of 5 rows from "tbl" using reservoir sampling
        return f" USING SAMPLE {nb_raw}"

    # ---------------------------------------------------------#
    # -------------- database SELECT queries ------------------#
    # ---------------------------------------------------------#
    def select_table(self, table_name: str, clause: str = '', expr: str = 'rowid, *') -> str:
        query = f"SELECT {expr} FROM {table_name}{clause}"
        return query

    # ---------------------------------------------------------#
    def select_table_updown(self, table_name: str, nb_rows: int) -> duckdb.DuckDBPyRelation:
        r1 = self.sql(self.select_table(table_name, clause=f" LIMIT {nb_rows}")).set_alias('r1')
        r2 = self.sql(self.select_table(table_name, clause=f" ORDER BY rowid DESC LIMIT {nb_rows}")).set_alias(
            'r2').order("rowid")

        return r1.union(r2)

    # ---------------------------------------------------------#
    # --------------- database conversions --------------------#
    # ---------------------------------------------------------#
    def conv_to_pandas(self, rel: duckdb.DuckDBPyRelation) -> pd.DataFrame:
        start_time = timeit.default_timer()
        pd = rel.fetchdf()
        stop_time = timeit.default_timer()
        logging.info("import took {}".format(stop_time - start_time))
        return pd

    # ---------------------------------------------------------#
    def conv_to_polars(self, rel: duckdb.DuckDBPyRelation) -> polars.DataFrame:
        start_time = timeit.default_timer()
        pl = rel.pl()
        stop_time = timeit.default_timer()
        logging.info("import took {}".format(stop_time - start_time))
        return pl

    # ---------------------------------------------------------#
    def conv_to_numpy(self, rel: duckdb.DuckDBPyRelation) -> dict:
        start_time = timeit.default_timer()
        np_dict = rel.fetchnumpy()
        stop_time = timeit.default_timer()
        logging.info("import took {}".format(stop_time - start_time))
        return np_dict

    # ---------------------------------------------------------#
    # --------------- database simple fct ---------------------#
    # ---------------------------------------------------------#
    def show_table(self, table: str) -> None:
        self.sql(self.select_table(table)).show()

    # ---------------------------------------------------------#
    def show_query(self, query: str) -> None:
        self.sql(query).show()

    # ---------------------------------------------------------#
    def show_rel(self, rel: duckdb.DuckDBPyRelation) -> None:
        start_time = timeit.default_timer()
        rel.show()
        stop_time = timeit.default_timer()
        logging.info("show rel took {}".format(stop_time - start_time))

    # ---------------------------------------------------------#
    def count_row(self, table_name: str, where_clause: str = '') -> int:
        query = f"SELECT COUNT(*) FROM {table_name}{where_clause}"
        result = self.sql(query).fetchone()[0]

        return result

    # ---------------------------------------------------------#
    def min(self, table_name: str, column_name: str, clause: str = '', only_value=True):
        query = f"SELECT MIN({column_name}) FROM {table_name}{clause}"
        result = self.sql(query).fetchone()[0]

        if not only_value:
            try:
                query = f"SELECT arg_min(rowid, {column_name}) FROM {table_name}{clause}"
                rowid = self.sql(query).fetchone()[0]
            except (Exception, duckdb.BinderException) as error:
                print(error)
                rowid = None
        else:
            rowid = None
        return rowid, result

    # ---------------------------------------------------------#
    def max(self, table_name: str, column_name: str, clause: str = '', only_value=True):
        query = f"SELECT MAX({column_name}) FROM {table_name}{clause}"
        result = self.sql(query).fetchone()[0]

        if not only_value:
            try:
                query = f"SELECT arg_max(rowid, {column_name}) FROM {table_name}{clause}"
                rowid = self.sql(query).fetchone()[0]
            except (Exception, duckdb.BinderException) as error:
                print(error)
                rowid = None
        else:
            rowid = None
        return rowid, result

    # ---------------------------------------------------------#
    def mean(self, table_name: str, column_name: str, clause: str = ''):
        query = f"SELECT MEAN({column_name}) FROM {table_name}{clause}"
        result = self.sql(query).fetchone()[0]

        return result

    # ---------------------------------------------------------#
    def var(self, table_name: str, column_name: str, clause: str = ''):
        query = f"SELECT VAR({column_name}) FROM {table_name}{clause}"
        result = self.sql(query).fetchone()[0]

        return result

    # ---------------------------------------------------------#
    def std(self, table_name: str, column_name: str, clause: str = ''):
        query = f"SELECT STDDEV({column_name}) FROM {table_name}{clause}"
        result = self.sql(query).fetchone()[0]

        return result

    # ---------------------------------------------------------#
    def project_numeric_fct(self, ini_query: str, fct: str) -> duckdb.DuckDBPyRelation:
        rel = self.sql(ini_query).set_alias('rel').project(fct)
        return rel

    # ---------------------------------------------------------#
    # --------------- database calcul fct ----------------------#
    # ---------------------------------------------------------#
    # ---------------------------------------------------------#
    def calcul_stats(self, table, column, where_expr='rowid', where_clause='', idx=None,
                     batch_table: str = None, b_idx=None, dataframe=True):

        expr = f"""MEAN(rowid) AS meanrowid, 
                       MIN({column}) AS min, MAX({column}) AS max, 
                       MEAN({column}) AS mean, 
                       VARIANCE({column}) AS var, 
                       STDDEV({column}) AS std, 
                       COUNT({column}) as count"""

        if idx is not None:
            recup = self.fetch_from_idx(table, idx=idx, expr=expr,
                                        where_expr=where_expr, where_clause=where_clause)
        elif b_idx is not None:
            if isinstance(b_idx, int):
                recup = self.fetch_from_batch(table,
                                              expr=expr,
                                              clause_supp=where_clause,
                                              b_idx=b_idx,
                                              batch_table_name=batch_table,
                                              dataframe=False)
            else:
                recup = self.fetch_from_batch(table,
                                              start_id=b_idx[0], end_id=b_idx[-1],
                                              expr=expr,
                                              clause_supp=where_clause,
                                              dataframe=dataframe)
        else:
            recup = self.fetch_signal(table, expr=expr, clause=where_clause)

        return recup

    # ---------------------------------------------------------#
    def calcul_stats_all_table(self, table, where_expr='rowid', where_clause='', idx=None,
                               batch_table: str = None, b_idx=None, dataframe=True):
        describe_result = self.sql(f"SELECT * FROM {table} LIMIT 1;")

        stats_dataframe = pd.DataFrame({})

        for k in range(np.shape(describe_result.description)[0]):
            column = describe_result.description[k][0]

            recup = pd.concat([pd.DataFrame({'source': [column]}),
                               self.calcul_stats(table, column, where_expr, where_clause, idx,
                                                 batch_table, b_idx, dataframe)], axis=1)

            stats_dataframe = pd.concat([stats_dataframe, recup], axis=0)

        stats_dataframe = stats_dataframe.set_index('source')
        return stats_dataframe

    # ---------------------------------------------------------#
    # --------------- database fetch fct ----------------------#
    # ---------------------------------------------------------#
    def fetch_batch_ids(self, table: str, b: int):
        rel = self.sql(self.select_table(table,
                                         clause=f" WHERE rowid={b}",
                                         expr='start_id, end_id'
                                         ))
        batch_ids = self.conv_to_pandas(rel)
        return batch_ids['start_id'].values[0], batch_ids['end_id'].values[0]

    # ---------------------------------------------------------#
    def fetch_signal(self, table: str, clause: str = '', expr: str = 'rowid, *') -> pd.DataFrame:
        return self.conv_to_pandas(self.sql(self.select_table(table, clause, expr)))

    # ---------------------------------------------------------#
    def fetch_from_idx(self, table, idx, expr: str = 'rowid, *', where_expr: str = 'rowid', where_clause: str = ''):
        rel = self.sql(self.select_table(table,
                                         clause=f" WHERE {where_expr}{self.conv_numpy_to_IN_clause(idx)}{where_clause}",
                                         expr=expr)).order('rowid')
        return self.conv_to_pandas(rel)

    # ---------------------------------------------------------#
    def fetch_from_other_table_idx(self, table, other_table, idx, expr: str = 'rowid, *', where_expr: str = 'rowid',
                                   where_clause: str = ''):
        rel = self.sql(self.select_table(table,
                                         clause=f""" WHERE rowid IN (
                                                        SELECT rowid FROM {other_table}
                                                        WHERE {where_expr}{self.conv_numpy_to_IN_clause(idx)}
                                                        ){where_clause}""",
                                         expr=expr)).order('rowid')
        return self.conv_to_pandas(rel)

    # ---------------------------------------------------------#
    def fetch_from_table_under_condition(self, table, other_table, condition, expr: str = 'rowid, *',
                                         where_expr: str = 'rowid',
                                         where_clause: str = ''):
        rel = self.sql(self.select_table(table,
                                         clause=f""" WHERE rowid IN (
                                                        SELECT {where_expr} FROM {other_table}
                                                        WHERE {condition}
                                                        ){where_clause}""",
                                         expr=expr)).order('rowid')
        return self.conv_to_pandas(rel)

    # ---------------------------------------------------------#
    def fetch_from_batch(self, table_name: str, start_id: int = 0, end_id: int = 0, expr: str = 'rowid, *',
                         clause_supp: str = '',
                         b_idx: int = None, batch_table_name: str = None, dataframe=True):

        if b_idx is not None:
            rel = self.sql(self.select_table(table_name,
                                             clause=f""" WHERE {table_name}.rowid >= (
                                                            SELECT start_id
                                                            FROM {batch_table_name}
                                                            WHERE rowid={b_idx}
                                                         ) AND {table_name}.rowid <= (
                                                            SELECT end_id
                                                            FROM {batch_table_name}
                                                            WHERE rowid={b_idx}
                                                         ){clause_supp}""",
                                             expr=expr))
        else:
            try:
                rel = self.sql(self.select_table(table_name,
                                                 clause=f" WHERE rowid >= {start_id} AND rowid <= {end_id}{clause_supp}",
                                                 expr=expr)).order('rowid')
            except (Exception, duckdb.BinderException) as error:
                logging.debug(error)
                rel = self.sql(self.select_table(table_name,
                                                 clause=f" WHERE {table_name}.rowid >= {start_id} AND {table_name}.rowid <= {end_id}{clause_supp}",
                                                 expr=expr))
        if dataframe:
            return self.conv_to_pandas(rel)
        else:
            return rel

    # ---------------------------------------------------------#
    def fetch_from_batch_under_condition(self, table: str, other_table: str, condition,
                                         start_id: int = 0, end_id: int = 0, expr: str = 'rowid, *',
                                         b_idx: int = None, batch_table: str = None):

        if b_idx is not None:
            clause_supp = f""" AND {table}.rowid >= (
                                    SELECT start_id
                                    FROM {batch_table}
                                    WHERE rowid={b_idx}
                               ) AND {table}.rowid <= (
                                    SELECT end_id
                                    FROM {batch_table}
                                    WHERE rowid={b_idx}
                               )"""
        else:
            clause_supp = f" AND rowid >= {start_id} AND rowid <= {end_id}"

        dataframe = self.fetch_from_table_under_condition(table, other_table,
                                                          condition,
                                                          expr=expr,
                                                          where_expr='rowid',
                                                          where_clause=clause_supp)
        return dataframe

    # ---------------------------------------------------------#
    def fetch_idx_table_from_batch(self, table_name: str, start_id: int, end_id: int, expr: str = 'rowid, *',
                                   phase_detection=False):
        if phase_detection:
            rel = self.sql(self.select_table(table_name,
                                             clause=f" WHERE start_id >= {start_id} AND start_id <= {end_id}",
                                             expr=expr)).order('rowid')
        else:
            rel = self.sql(self.select_table(table_name,
                                             clause=f" WHERE start_id >= {start_id} AND end_id <= {end_id}",
                                             expr=expr)).order('rowid')
        return self.conv_to_pandas(rel)

    # ---------------------------------------------------------#
    def fetch_idx_table_from_batch_under_condition(self, table: str, other_table: str, condition,
                                                   start_id: int, end_id: int, expr: str = 'rowid, *',
                                                   phase_detection=False):
        if phase_detection:
            dataframe = self.fetch_from_table_under_condition(table, other_table,
                                                              condition,
                                                              expr=expr,
                                                              where_expr='number',
                                                              where_clause=f""" AND start_id >= {start_id} AND start_id <= {end_id}""")
        else:
            dataframe = self.fetch_from_table_under_condition(table, other_table,
                                                              condition,
                                                              expr=expr, where_expr='number',
                                                              where_clause=f""" AND start_id >= {start_id} AND end_id <= {end_id}""")
        return dataframe

    # ---------------------------------------------------------#
    def fetch_from_list(self, table, idx, num=None, expr: str = 'rowid, *', where_expr: str = 'rowid', where_clause: str = ''):
        query = f"""WITH evtidx AS (SELECT unnest({idx.tolist()}) AS id, unnest({num.tolist()}) AS n)
                        SELECT rowid, n, * 
                        FROM evtidx JOIN {table} ON {table}.rowid = id
                        """
        rel = self.sql(query).order('n')
        return self.conv_to_pandas(rel)
