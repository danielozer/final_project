#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
-----------------------------------------------------------------------------
Author          :   Yaniv Nana
Filename        :   db_sqlite.py
Date            :   Aug 4 2016.
Version         :   1.0
Exercise Number :   project "os-training"
Description     :   basic sql-lite database functionality.
-----------------------------------------------------------------------------
"""

import sqlite3 as lite
import sys

dbg_mode = 0



# *****************************************************************************
def gen_db(db_fname, tbl_name, col_name_type, tbl_values):
    """ function to generate an SQL lite database.
    """
    print col_name_type.split(' ')
    num_of_items = len(col_name_type.split(' '))
    print "num_of_items : "+str(num_of_items)
    row0 = list(tbl_values)[0]
    print "l1: "+str(row0)
    row0 = list(row0)
    print "l2: "+str(row0)

    print 0x1
    print len(row0)
    print num_of_items/2

    if num_of_items & 0x1 or len(row0) != (num_of_items/2):
        print "error: in argument 'col_name_type'.."
        return(True)
    else:
        qmarks = ""
        for x in range(num_of_items/2):
            qmarks = qmarks +" ?,"
        qmarks = qmarks[0:len(qmarks)-1]

    db_conn = lite.connect(db_fname)

    with db_conn:
        cur = db_conn.cursor()
        query = "DROP TABLE IF EXISTS {tn}".format(tn=tbl_name)
        cur.execute(query)
        query = "CREATE TABLE {tn} ({cnt})".format(tn=tbl_name,cnt=col_name_type)
        cur.execute(query)
        query = "INSERT INTO {tn} VALUES({qm})".format(tn=tbl_name,qm=qmarks)
        cur.executemany(query, tbl_values)
        db_conn.commit()




# *****************************************************************************
def query_db(db_name, query, return_mode):
    """ query_db function to query the database and metadata.
    """
    str_percS = ""
    retval = True

    db_conn = lite.connect(db_name)

    with db_conn:
        db_conn.row_factory = lite.Row
        cur = db_conn.cursor()
        try:
            cur.execute(query)
            if return_mode == 'r':
                db_conn.commit()

        except lite.OperationalError or lite.ValuelError as e:
            print "SQL-lite3 error:"
            print e
            if 'r' == return_mode:
                retval = False

    if 'nr' == return_mode:
        pass
    elif 'r' == return_mode:
        # col_names = [cn[0] for cn in cur.description]
        # num_names = len(col_names)
        # for i in range(num_names):
        #     str_percS = str_percS + "%-10s "
        rows = cur.fetchall()

        # if dbg_mode:
        #     if len(rows[0])==1:
        #         print list(rows)
        #     else:
        #         print str_percS % tuple(col_names)
        #         for row in rows:
        #             print str_percS % row
        if False == retval:
            return(retval)
        else:
            return(rows)


# *****************************************************************************
def update_tbl(db_name, query, new_vaule):
    """ update the
    """

    db_conn = lite.connect(db_name)

    with db_conn:
        db_conn.row_factory = lite.Row
        cur = db_conn.cursor()

        #cur.execute("UPDATE Cars SET Price=? WHERE Id=?", (uPrice, uId))
        cur.execute(query, new_vaule)
        db_conn.commit()

        if dbg_mode:
            print "Number of rows updated: %d" % cur.rowcount





# *****************************************************************************
def total_rows(fname, table_name, print_out=False):
    """ Returns the total number of rows in the database """
    db_conn = lite.connect(fname)
    with db_conn:
        cur = db_conn.cursor()
        cur.execute('SELECT COUNT(*) FROM {}'.format(table_name))
        count = cur.fetchall()
        if print_out:
            print('\nTotal rows: {}'.format(count[0][0]))
    return count[0][0]



# # *****************************************************************************

# def connect(db_path_fname):
#     """ Make connection to an SQLite database file """
#     db_conn = lite.connect(db_path_fname)
#     with db_conn:
#     	cur = db_conn.cursor()
#     return db_conn, cur


# # *****************************************************************************
# def close(db_conn):
#     """ Commit changes and close connection to the database """
#     # db_conn.commit()
#     db_conn.close()


# # *****************************************************************************
# def table_col_info(cursor, table_name, print_out=False):
#     """ Returns a list of tuples with column informations:
#         (id, name, type, notnull, default_value, primary_key)
#     """
#     db_conn = lite.connect(db_name)
#     with db_conn:
#     	cur = db_conn.cursor()
# 	    cur.execute('PRAGMA TABLE_INFO({})'.format(table_name))
# 	    info = cur.fetchall()

# 	    if print_out:
# 	        print("\nColumn Info:\nID, Name, Type, NotNull, DefaultVal, PrimaryKey")
# 	        for col in info:
# 	            print(col)
#     return info


# # *****************************************************************************
# def values_in_col(cursor, table_name, print_out=True):
#     """ Returns a dictionary with columns as keys and the number of not-null
#         entries as associated values.
#     """
#     db_conn = lite.connect(db_name)
#     with db_conn:
# 	    cur = db_conn.cursor()
# 	    cur.execute('PRAGMA TABLE_INFO({})'.format(table_name))
# 	    info = cur.fetchall()
# 	    col_dict = dict()
# 	    for col in info:
# 	        col_dict[col[1]] = 0
# 	    for col in col_dict:
# 	        cur.execute('SELECT ({0}) FROM {1} WHERE {0} IS NOT NULL'.format(col, table_name))
# 	        # In my case this approach resulted in a better performance than using COUNT
# 	        number_rows = len(cur.fetchall())
# 	        col_dict[col] = number_rows
# 	    if print_out:
# 	        print("\nNumber of entries per column:")
# 	        for i in col_dict.items():
# 	            print('{}: {}'.format(i[0], i[1]))
# 	    return col_dict





""" Transactions:
    ------------
In SQLite, any command other than the SELECT will start an implicit transaction.
Also, within a transaction a command like CREATE TABLE ..., VACUUM, PRAGMA, will
commit previous changes before executing.
Manual transactions are started with the BEGIN TRANSACTION statement and finished
with the COMMIT or ROLLBACK statements.
SQLite supports three non-standard transaction levels: DEFERRED, IMMEDIATE and
EXCLUSIVE.
SQLite Python module also supports an autocommit mode, where all changes to the
tables are immediately effective. """






