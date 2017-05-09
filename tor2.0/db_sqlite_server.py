__author__ ="daniel ozer"
import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:

        conn = sqlite3.connect(db_file)
        print "fine"
        return conn
    except :
        print("error")

    return None


def msg_disassembly (mesg):
    #should check next time if the mesg has checksum
    mesg=mesg.split("|")
    if len(mesg)==4:

        mesg.remove(mesg[0])
        print mesg

        return mesg
    else:
        return "error!!"


def insert_new_conn(database,data):

    database = "E:\music\server_db.db"
    data=['219.199.100.1','20.99.11.99','ASD112S','20.99.11.99~20.99.11.99~20.99.11.99' ]
    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        cur=conn.cursor()
        # create projects table
        cur.execute("INSERT INTO ips_conn_id VALUES (?,?,?,?)",data)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
    conn.close()

def get_the_list(database,conn_id):
    data=[]

    conn = create_connection(database)
    if conn is not None:
        cur=conn.cursor()
        # create projects table
        for row in cur.execute('SELECT * FROM server_db_data '):
            data.insert(len(data),row)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
    conn.close()
    print data
    return data

