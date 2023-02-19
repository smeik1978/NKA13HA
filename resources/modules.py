#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 19:17:31 2022

@author: matthias
"""

import sqlite3

import pandas as pd
from pandas.tseries.offsets import Day
from PySide6 import QtGui
from PySide6.QtCore import Qt


def fetch_db_pd(t):
    try:
        conn = sqlite3.connect('standard.sqlite')
        pd_tmp = pd.read_sql("SELECT * FROM " + t + ";", conn)
    
    except sqlite3.Error as error:
        print("Fehler beim Laden in Dataframe", error)

    finally:
        if conn:
            conn.close()
    return pd_tmp

def fetch_data(table,id):
    """
    Liest einen Datensatz aus einer tabelle
    :param table:
    :param id:
    :return: data
    """
    try:
        database = 'standard.sqlite'
        conn = create_connection(database)
        cur = conn.cursor()
        sql = 'SELECT * FROM {} WHERE id = {}'.format(table, id)
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        
    except sqlite3.Error as error:
        print("fetch_data. Fehler beim Ausführen der SQL Query:",error)
    finally:
        if conn:
            conn.close()
    return data

def fetch_data2(table, key, value):
    try:
        value += 0
    except TypeError as error:
        value = "'" + value + "'"

    try:
        database = 'standard.sqlite'
        conn = create_connection(database)
        cur = conn.cursor()
        sql = 'SELECT * FROM {} WHERE {} = {}'.format(table, key, value)
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        
    except sqlite3.Error as error:
        print("fetch_data2. Fehler beim Ausführen der SQL Query:",error)
       
    finally:
        if conn:
            conn.close()
    return data
    
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as error:
        print("Fehler beim Verbinden mit der Datenbank",error)

    return conn

def create_sql_schema():
    d_schema = {}
    database = 'standard.sqlite'
    conn = create_connection(database)
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
    if len(keys)>1:
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
    else:
        insert = keys[0]
        update = keys[0]
        update += " = ?"
        query = {}
        query['insert'] = "INSERT INTO "+t+"("+insert+") VALUES(?)"
        query['update'] = "UPDATE "+t+" SET "+update+" WHERE id = ?"
    return query
  
def sql_insert(table_name, data):
    """
    Erstellt einen neuen Eintrag in einer Tabelle
    :param :
    :return: db id
    """
    try:
        database = 'standard.sqlite'
        conn = create_connection(database)
        query = query_structure(table_name)
        sql = query['insert']
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    
    except sqlite3.Error as error:
        print("SQLite Fehler beim INSERT",error)
        
    finally:
        if conn:
            conn.close()
    return cur.lastrowid

def sql_update(table_name,data):
    try:
        database = 'standard.sqlite'
        conn = create_connection(database)
        cur = conn.cursor()
        query = query_structure(table_name)
        sql = query['update']
        cur.execute(sql, data)
        conn.commit()
        cur.close()

    except sqlite3.Error as error:
        print("SQLite Fehler beim UPDATE",error)
    finally:
        if conn:
            conn.close()
    
class PandasModel(QtGui.QStandardItemModel):
    def __init__(self, data, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        self._data = data
        for col in data.columns:
            data_col = [QtGui.QStandardItem("{}".format(x)) for x in data[col].values]
            self.appendColumn(data_col)
        return

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def headerData(self, x, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[x]
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._data.index[x]
        return None

def kosten():
    pdData = fetch_db_pd('Kosten')
    pdData = pdData.sort_values('Kostenart')
    pdData['Betrag'] = pdData["Betrag"].str.replace(',', '.') 
    pdData['Betrag'] = pdData["Betrag"].astype('float')    
    grouped = pdData.groupby(['Abrechnungsjahr', 'Kostenart'], as_index=False)['Betrag'].sum()
    return grouped


def kostenEinheit():
    pdData = fetch_db_pd('Kosten')
    pdData['Betrag'] = pdData["Betrag"].str.replace(',', '.') 
    pdData['Betrag'] = pdData["Betrag"].astype('float')
    m = pdData['Menge'].str.contains(',',na=False)
    pdData.loc[m, 'Menge'] = pdData.loc[m, 'Menge'].str.replace(',', '.') 
    pdData['Menge'] = pdData["Menge"].astype('float')
    pdData['Kosten/Einheit'] = pdData['Betrag'] / pdData['Menge']
    return pdData

### Export Forms
def expForms():
    conn = sqlite3.connect('nebenkosten.db')
    dfAblesung = pd.read_sql("SELECT * FROM Ablesung", conn, index_col='index')
    dfAblesung.fillna(value='00000', inplace=True)
    
    dfFilter = pd.DataFrame()
    dfFilter['ID']  = dfAblesung['WEID']
    dfFilter.drop_duplicates(inplace=True)
    
    for index,row in dfFilter.iterrows():
        dfTmp = dfAblesung.loc[dfAblesung['WEID'] == row[0]][['WEID','Ort', 'Zählertyp', 'Zählernummer', 'Endstand']]
        dfTmp['Stand Ablesung'] = ""
        #filename = row[0] + '.xlsx'
        writer = pd.ExcelWriter(row[0] + '.xlsx') 
        dfTmp.to_excel(writer, sheet_name='Ablesung', index=False, na_rep='NaN')
    
        # Auto-adjust columns' width
        for column in dfTmp:
            column_width = max(dfTmp[column].astype(str).map(len).max(), len(column))
            col_idx = dfTmp.columns.get_loc(column)
            writer.sheets['Ablesung'].set_column(col_idx, col_idx, 14)#column_width)
        writer.save()
    conn.close()
    
def main():
    pass
    
    schema = create_sql_schema()
    entries_to_remove = ('sqlite_sequence', 'Umlageschluessel')
    for k in entries_to_remove:
        schema.pop(k, None)
    tables = list(schema.keys())
    #keys.remove('sqlite_sequence')
    print(schema)
    print(tables)
    columns = list(schema[tables[4]])
    columns.pop(0)
    print(columns)

        
if __name__ == '__main__':
    main()