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



def main():
    database = "E:\music\client_db.db"

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        cur=conn.cursor()
        # create projects table
        cur.execute("INSERT INTO client_db_data (sender_name,recv_date,conn_id,mesg_data) \
      VALUES ('daniel','20/10/10','ASD112S','what a nice day' )")
        conn.commit()
    else:
        print("Error! cannot create the database connection.")



main()