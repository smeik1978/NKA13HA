import sqlite3 as sqlite


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite.connect(db_file)
    except sqlite.Error as e:
        print(e)

    return conn


def create_wohnung(conn, wohnung):
    """
    Erstellt einen neuen Eintrag in der Wohnungen Tabelle
    :param conn:
    :param wohnung:
    :return: wohnung id
    """
    sql = ''' INSERT INTO Wohnungen(Nummer, Stockwerk, qm, Zimmer)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, wohnung)
    conn.commit()
    return cur.lastrowid