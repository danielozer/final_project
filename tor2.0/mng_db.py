"""
-----------------------------------------------------------------------------
Author          :   Yaniv Nana
Filename        :   mng_db.py
Date            :   Aug 4 2016.
Version         :   1.0
Exercise Number :   project "os-training"
Description     :   basic sql-lite database functionality.
-----------------------------------------------------------------------------
"""

import os
import sys
from db_sqlite import *



db_path = r'C:\Cyber\final_os\proj'
db_fname = 'userpass.db'
db_path_fname = db_path + '\\' + db_fname



col_name_type1 = "Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, SupperUserFlag INT, UserHash TEXT, PasswordHash TEXT"
tbl_name1 = "srvr_users"
# Id, user-ID-name, supper-user-flag, srvr-password-hashed
init_spass_db = (
    (1, 'yaniv nana', 1, -1, -1),
    (2, 'yossi cohen', 1, -1, -1),
    (3, 'miki epstein', 0, -1, -1),
    (4, 'rami verbin', 0, -1, -1),
    (5, 'ziv tepper', 0, -1, -1))



# INTEGER PRIMARY KEY AUTOINCREMENT
# PRIMARY KEY(Name,ApplName)
col_name_type2 = "Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, ApplName TEXT, User TEXT, Password TEXT"
tbl_name2 = "passwords_records"
# Id, user-ID-name, appl-name, user-hashed, password-hashed
init_upass_db = (
    (1, 'yaniv nana', 'nana10', -1, -1),
    (2, 'yossi cohen', 'nrg', -1, -1),
    (3, 'miki epstein', 'ynet', -1, -1),
    (4, 'rami verbin', 'themarker', -1, -1),
    (5, 'rami verbin', 'israel hayom', -1, -1),
    (6, 'yaniv nana', 'ynet', -1, -1),
    (7, 'ziv tepper', 'ebay', -1, -1))



# *****************************************************************************
def init_db(fname):
    """ initialize database for {user \ password \ application} records
    """

    if os.path.isfile(fname):
        print "database exists.. passing on.."
        # return(1)
    else:
        print "database do not exists, generating.."
        gen_db(fname, tbl_name1, col_name_type1, init_spass_db)
        gen_db(fname, tbl_name2, col_name_type2, init_upass_db)



# *****************************************************************************
def extract_table(fname, table_name):
    """ extract from database the hole table record
    """

    query = "SELECT * FROM {tn}".format(tn=table_name)
    rows = query_db(fname, query, 'r')
    return(rows)




# *****************************************************************************
def query_sys_match(hash_user, hash_pass):
    """ query in system table to find match: {hash_user, hash_pass},
        return the number of row records.
    """
    query = "SELECT * FROM {tn} WHERE {cn1}='{cn1v}' and {cn2}='{cn2v}'".\
        format(tn=tbl_name1, cn1="UserHash", cn2="PasswordHash", cn1v=hash_user, cn2v=hash_pass)
    rows = query_db(db_path_fname, query, 'r')

    num_of_rows = len(rows)
    if 1 == num_of_rows:
        (Id, uname, supper_user, user_hash, pass_hash)= rows[0]
        return((num_of_rows, uname))
    else:
        return((num_of_rows, ""))



# *****************************************************************************
def get_up_by_appl(appl_name, name):
    """ query in allpication table to find {appl_name, uname},
        return: {user, pass} records.
    """
    query = "SELECT * FROM {tn} WHERE {cn1}='{cn1v}' and {cn2}='{cn2v}'".\
            format(tn=tbl_name2, cn1="Name", cn2="ApplName", cn1v=name, cn2v=appl_name)
    rows = query_db(db_path_fname, query, 'r')
    num_of_rows = len(rows)

    if 1 == num_of_rows:
        (Id, name, appl_name, username, password)= rows[0]
        user_pass = [username, password]
        return((num_of_rows, username, password))
    else:
        return((num_of_rows, "", ""))


# *****************************************************************************
def updt_up_by_appl(name, appl_name, username, password):
    """ update application table to find {name, appl_name}, updates {user, pass} records.
        return: True/False
    """
    query1 = "UPDATE {tn} SET {cn1}=('{cn1v}') WHERE {cn3}=('{nm}') and {cn4}=('{ap}')".\
            format(tn=tbl_name2,cn1="User",cn1v=username,cn3="Name",nm=name,cn4="ApplName",ap=appl_name)
    query2 = "UPDATE {tn} SET {cn2}=('{cn2v}') WHERE {cn3}=('{nm}') and {cn4}=('{ap}')".\
            format(tn=tbl_name2,cn2="Password",cn2v=password,cn3="Name",nm=name,cn4="ApplName",ap=appl_name)
    query3 = "SELECT * FROM {tn} WHERE {cn3}=('{nm}') and {cn4}=('{ap}')".\
            format(tn=tbl_name2,cn3="Name",nm=name,cn4="ApplName",ap=appl_name)

    query_db(db_path_fname, query1, 'nr')             # updates User Column
    query_db(db_path_fname, query2, 'nr')             # updates Password Column
    rows = query_db(db_path_fname, query3, 'r')       # Verify both fields
    num_of_rows = len(rows)

    retval = False
    if 1 == num_of_rows:
        if username in rows[0] and password in rows[0]:
            retval = True
    return(retval)



# *****************************************************************************
def insrt_up_by_appl(name, appl_name, username, password):
    """ inserts application-table new record
        return: True/False{uname, appl_name, hash_user, hash_pass} records.
    """
    query1 = "SELECT * FROM {tn} WHERE {cn3}=('{nm}') and {cn4}=('{ap}')".\
            format(tn=tbl_name2,cn3="Name",nm=name,cn4="ApplName",ap=appl_name)
    rows = query_db(db_path_fname, query1, 'r')       # Verify both fields
    num_of_rows = len(rows)

    if 0 == num_of_rows:
        row_max = total_rows(db_path_fname, tbl_name2, print_out=False)
        query = "INSERT INTO {tn} (Id, Name, ApplName, User, Password) VALUES(NULL,'{nm}','{an}','{un}','{pw}')".\
                format(tn=tbl_name2,nm=name,an=appl_name,un=username,pw=password)
        rows = query_db(db_path_fname, query, 'r')
        nor = len(rows)

        row_max_end = total_rows(db_path_fname, tbl_name2, print_out=False)
        retval = (row_max_end-1 == row_max)
    else:
        retval = num_of_rows
    return(retval)


# *****************************************************************************
def get_num_usr_rcrds(name):
    """ get number of application-records in table per user
        return: {number of records per user}.
    """
    # cnt = 0
    query = "SELECT {cn1} FROM {tn} WHERE {cn2}='{nm}'".format(tn=tbl_name2,cn1="Id",cn2="Name",nm=name)
    rows = query_db(db_path_fname, query, 'r')
    num_of_rcrds = len(rows)

    return(num_of_rcrds)




# # *****************************************************************************
# def main():
#     """ main function implements the main of the save-my-cb.
#     """
#
#
#
#
# if __name__ == "__main__":
#     main()




# # *****************************************************************************
# def extract_by_two(fname, tn1, cn1, cn2, cv1, cv2):
#     """ extract row record from database by two columns: {user-ID-name, application}
#     """
#     query = "SELECT * FROM {tn} WHERE {cn}==?".format(tn=tn1, cn=cn1)
#     rows = query_dict_db(fname, query, (cv1,))

#     retval = False
#     for row in rows:
#         # print row[cn2]
#         if row[cn2] == cv2:
#             retval = row
#             break
#     return(retval)


# # *****************************************************************************
# def update_record(fname, tbl_name, up_cn, up_val, Id):
#     """ extract from database by two columns: {user-ID-name, application} row records
#     """
#     query = "UPDATE {tn} SET {cn}=? WHERE Id=?".format(tn=tbl_name, cn=up_cn)
#     updt_db(fname, query, (up_val, Id))
#     query = "SELECT * FROM {tn} WHERE Id=?".format(tn=tbl_name)
#     rows = query_dict_db(fname, query, (Id,))

#     return(rows)


# # *****************************************************************************
# def insert_record(fname, tbl_name, row_values):
#     """ insert database new row record.
#     """
#     Id = total_rows(fname, tbl_name, print_out=False) ; Id += 1
#     row_values = list(row_values) ; row_values[0] = Id ; row_values = tuple(row_values)

#     query = "INSERT OR IGNORE INTO {tn} VALUES(?, ?, ?, ?, ?)".format(tn=tbl_name)
#     insert_db(fname, query, row_values)
#     query = "SELECT * FROM {tn} WHERE Id=?".format(tn=tbl_name)
#     rows = query_dict_db(fname, query, (Id,))

#     return(rows)
