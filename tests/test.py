import sqlite3
import pandas as pd

db = './standard.sqlite'
def readSingleRow(Id):
    try:
        sqliteConnection = sqlite3.connect(db)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from Wohnungen where id = ?"""
        cursor.execute(sqlite_select_query, (Id,))
        print("Reading single row \n")
        record = cursor.fetchone()
        print("Id: ", record[0])
        print("Name: ", record[1])
        print("Email: ", record[2])
        print("JoiningDate: ", record[3])
        print("Salary: ", record[4])

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read single row from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def create_sql_schema():
    d_schema = {}
    conn = conn = sqlite3.connect(db)
    cur = conn.cursor()
    table = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
    for index, row in table.iterrows():
        pd_meta = pd.read_sql_query("PRAGMA table_info("+row['name']+")",conn, index_col='cid')
        d_schema[row['name']] = dict(zip(pd_meta['name'],pd_meta['type']))
    conn.close()
    return d_schema
    
def query_structure(t):
    schema = create_sql_schema()
    table = schema[t]
    keys = list(table)
    keys.remove('id')
    insert = ' '.join(keys)
    update = ' '.join(keys)
    insert = insert.replace(" ",", ")
    update = update.replace(" "," = ?, ")
    update += " = ?"
    qmrks = ""
    for i in range(len(keys)):
        qmrks += "?,"
    qmrks = qmrks[0:-1]
    query = {}
    query['insert'] = "INSERT INTO "+t+"("+insert+") VALUES("+qmrks+")"
    query['update'] = "UPDATE "+t+" SET "+update+" WHERE id = ?"
    return query
    
test = query_structure('Wohnungen')
print(test['update'])
# """Update Wohnungen set Nummer = ?, Stockwerk = ?, qm = ?, Zimmer = ? where id = ?"""
   # sql = ''' INSERT INTO Vermietung(WEID, Wohnung, Vorname, Name, Strasse, Hausnummer, Plz, Ort, Mietbeginn, Mietende, Personen)
   #            VALUES(?,?,?,?,?,?,?,?,?,?,?) '''