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
        print("Verbindung zu SQLite hergestellt")
        pd_tmp = pd.read_sql("SELECT * FROM " + t + ";", conn)
    
    except sqlite3.Error as error:
        print("Fehler beim Laden in Dataframe", error)

    finally:
        if conn:
            conn.close()
            print("SQLite geschlossen")
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
        print("Daten erfolgreich eingelesen")
        cur.close()
        
    except sqlite3.Error as error:
        print("fetch_data. Fehler beim Ausführen der SQL Query:",error)
    finally:
        if conn:
            conn.close()
            print("SQLite geschlossen")
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
        print("Verbindung zu SQLite hergestellt")
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
        print("SQLite INSERT erfolgreich")
    
    except sqlite3.Error as error:
        print("SQLite Fehler beim INSERT",error)
        
    finally:
        if conn:
            conn.close()
            print("SQLite geschlossen")
    return cur.lastrowid

def sql_update(table_name,data):
    print(data)
    try:
        database = 'standard.sqlite'
        conn = create_connection(database)
        cur = conn.cursor()
        query = query_structure(table_name)
        sql = query['update']
        cur.execute(sql, data)
        conn.commit()
        print("SQLite UPDATE erfolgreich")
        cur.close()

    except sqlite3.Error as error:
        print("SQLite Fehler beim UPDATE",error)
    finally:
        if conn:
            conn.close()
            print("SQLite geschlossen")
    
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
    

def impdata():
    # Tabellen designen
    global dfWohnung, dfGemeinschaftsraum, dfHauptmieter, dfZaehler, dfZaehlertypen, dfKostenarten, dfKosten, dfEinheiten
    global dfUmlageschluessel, dfKonstanten, dfAblesung, dfVerbrauch, dfBerechnungen, dfZaehlerstand, dfKostenhistorie
    dfWohnung = pd.DataFrame(
        columns=('Nummer', 'Stockwerk', 'Größe qm', 'Anzahl Zimmer'))
    dfGemeinschaftsraum = pd.DataFrame(data=(
        'Küche', 'Bad', 'Büro', 'Gemeinschaftsraum'), columns=['Gemeinschaftsraum'])
    dfHauptmieter = pd.DataFrame(columns=('WEID', 'Wohnung', 'Vorname', 'Name',
                                 'Straße', 'PLZ', 'Ort', 'Mietbeginn', 'Mietende', 'Anzahl Personen'))
    dfZaehler = pd.DataFrame(columns=('Nummer', 'Typ', 'Gemeinschaft', 'Ort'))
    dfZaehlertypen = pd.DataFrame(
        data=('Kaltwasser', 'Warmwasser', 'Heizung', 'Strom'), columns=['Typ'])
    dfKostenarten = pd.DataFrame(data=('Müll', 'Kabelanschluss', 'Aufzug', 'Strom', 'Fernwärme', 'Kaltwasser', 'Warmwasser', 'Schmutzwasser',
                                 'Niederschlagswasser', 'Versicherung', 'Wartung', 'Gebühren', 'Steuer', 'Schädlingsbekämpfung', 'Salz'), columns=['Kostenart'])
    dfKosten = pd.DataFrame(columns=('Kostenart', 'Firma',
                            'Leistung', 'Betrag(€)', 'Menge', 'Einheit', 'Jahr'))
    dfEinheiten = pd.DataFrame(
        data=('m3', 'KWh', 'MWh', 'Stück'), columns=['Einheit'])
    dfUmlageschluessel = pd.DataFrame(data=(
        'Personen x Tage', 'Anzahl Wohneinheiten', 'Ablesung'), columns=['Schlüssel'])
    dfKonstanten = pd.DataFrame(
        data={'Konstante': ['Temperatur Warmwasser'], 'Wert': [60]})
    dfAblesung = pd.DataFrame(columns=(
        'Datum', 'WEID', 'Ort', 'Zählertyp', 'Zählernummer', 'Anfangsstand', 'Endstand'))
    dfVerbrauch = pd.DataFrame(
        columns=('WEID', 'Zählernummer', 'Typ', 'Verbrauch', 'Kosten'))
    dfBerechnungen = pd.DataFrame(columns=('Bezeichnung', 'Wert'))
    dfZaehlerstand = dfAblesung
    dfKostenhistorie = dfKosten
    

    # Daten aus NK2021 einlesen
    dfImportKosten = pd.read_excel(
        '~/Dokumente/Python/NKA13HA/Nebenkostenabrechnung_2021_Vs2_MM.xlsm', sheet_name=2)
    dfImportKosten.drop(columns=['Konto Lexware', 'Umlage', 'Erfasst',
                        'Betrag 2020', 'Bemerkung 2019', ' '], inplace=True)
    dfImportKosten.drop(index=[8, 9, 37, 38, 39, 40], inplace=True)
    dfImportKosten.rename(columns={'Betrag 2021': 'Betrag'}, inplace=True)
    dfImportKosten['Betrag'].fillna(0, inplace=True)
    dfImportKosten['Betrag'].replace(to_replace=" ", value=0, inplace=True)
    dfImportKosten['Menge'] = 0
    dfImportKosten['Jahr'] = '31.01.2021'
    dfImportKosten.loc[10, 'Menge'] = dfImportKosten.loc[11, 'Betrag']
    dfImportKosten.loc[14, 'Menge'] = dfImportKosten.loc[15, 'Betrag']
    dfImportKosten.loc[16, 'Menge'] = dfImportKosten.loc[17, 'Betrag']
    dfImportKosten.loc[22, 'Menge'] = dfImportKosten.loc[23, 'Betrag']
    dfImportKosten.loc[26, 'Menge'] = dfImportKosten.loc[27, 'Betrag']
    dfImportKosten.drop(index=[11, 12, 13, 15, 17, 18,
                        19, 20, 21, 23, 24, 25, 27, 28, 29], inplace=True)
    dfImportKosten.fillna("", inplace=True)
    
    dfImportMieter = pd.read_excel(
        'Nebenkostenabrechnung_2021_Vs2_MM.xlsm', sheet_name=4)
    dfImportMieter.rename(columns={'Anzahl Vermietungen': 'Stockwerk', 27: 'WEID', 3: 'Nummer', 'Unnamed: 3': 'Bewohner', 'Unnamed: 4': 'Mietbegin', 'Unnamed: 5': 'Mietende', 'Unnamed: 6': 'AnzahlTage', 'Unnamed: 7': 'Wohnfläche', 'Unnamed: 8': 'Personen', 'Aktuelle Vorauszahlung': 'Vorauszahlung',
                          'Unnamed: 10': 'Anzahl', 'Unnamed: 11': 'Gesamt', 'Unnamed: 12': 'Kaltwasser m3', 'Unnamed: 13': 'Warmwasser m3', 'Unnamed: 14': 'Verbrauch ista', 'Unnamed: 15': 'Nach/Rückzahlung', 'Neue Vorauszahlung': 'VZ Neu', 'Unnamed: 17': 'VZ Empfohlen', 'Unnamed: 18': 'VZ Differenz'}, inplace=True)
    dfImportMieter.drop(columns=['Unnamed: 19', 'Unnamed: 20',
                        'Unnamed: 21', 'Unnamed: 22', 'Unnamed: 23'], inplace=True)
    dfImportMieter.drop(index=0, inplace=True)
    dfImportMieter.drop(dfImportMieter.index[34:41], inplace=True)
    # dfImportMieter.set_index('WEID',inplace=True)
    
    #dfImportBelegung = pd.read_excel(
     #   'Nebenkostenabrechnung_2021_Vs2_MM.xlsm', sheet_name=5, dtype='object')
    
    dfImportStrom = pd.read_excel(
        'Nebenkostenabrechnung_2021_Vs2_MM.xlsm', sheet_name=8, dtype='object',)
    dfStrom = dfImportStrom.iloc[:, lambda df: [0, 1, 2, 4, 5]].copy()
    dfStrom.columns = ['Ort', 'ID', 'Zähler', 'Anfangsstand', 'Endstand']
    dfStrom.drop(index=[0, 1], inplace=True)
    dfStrom.dropna(inplace=True)
    #dfStrom.loc[2, ['Endstand']] = dfStrom.loc[2,['Endstand']].str.replace(',', '.')
    dfStrom['Anfangsstand'] = dfStrom['Anfangsstand'].astype('float')
    dfStrom['Endstand'] = dfStrom['Endstand'].astype('float')
    
    # Entfällt später, nur einmalig zum befüllen der Tabllen Stammdaten, Zähler etc. pp sowie als Beispiel zur Berechnung
    dfImportAblesung = pd.read_excel(
        'Nebenkostenabrechnung_2021_Vs2_MM.xlsm', sheet_name=9, dtype='object')
    dfImportAblesung = dfImportAblesung.drop(
        columns=['Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Verbrauch Kaltwasser', 'Verbrauch Warm', 'Verbrauch Ista'])
    dfImportAblesung.rename(columns={'Seriennummer': 'Zähler',
                            'Wert 31.12.2021': 'Endstand', 'Wert 31.12.2020': 'Anfangsstand'}, inplace=True)
    dfImportAblesung.drop(dfImportAblesung.index[362:367], inplace=True)
    dfImportAblesung.loc[dfImportAblesung['Typ'].str.contains(
        'ista'), 'Anfangsstand'] = 0
    dfImportAblesung['Endstand'] = dfImportAblesung['Endstand'].fillna(0)
    dfImportAblesung['Anfangsstand'] = dfImportAblesung['Anfangsstand'].astype(
        'float')
    # Zukünftig muss die Ablesung komplett in einer Tabelle erfolgen. Siehe Import-Vorlage
    
    #dfImportTemplate = pd.read_excel(
     #   'Nebenkostenabrechnung_2021_Vs2_MM.xlsm', sheet_name=6, dtype='object')
    
    
    #Tabellen befüllen
    ## Wohnungen
    grouped = dfImportMieter.groupby(by='Nummer').max()
    for name, group in grouped.iterrows():
        new_row = {'Nummer': name,
                   'Stockwerk': group[0], 'Größe qm': group[6], 'Anzahl Zimmer': ''}
        dfWohnung = pd.concat([dfWohnung,pd.DataFrame([new_row])], ignore_index=True)
    
    ## Hauptmieter
    grouped = dfImportMieter.groupby(by='WEID').max()
    for name, group in grouped.iterrows():
        new_row = {'WEID': name, 'Wohnung': group[1], 'Vorname': '', 'Name': group[2], 'Straße': 'Turleyplatz 8-9',
                   'PLZ': '68167', 'Ort': 'Mannheim', 'Mietbeginn': group[3], 'Mietende': group[4], 'Anzahl Personen': group[7]}
        dfHauptmieter = pd.concat([dfHauptmieter,pd.DataFrame([new_row])], ignore_index=True)
    
    ## Zähler
    grouped = dfImportAblesung.groupby(by='Zähler').max()
    for name, group in grouped.iterrows():
        for index, row in dfHauptmieter.iterrows():
            if group[0] == row[0]:
                new_row = {'Nummer': name,
                           'Typ': group[3], 'Gemeinschaft': 'N', 'Ort': row[1]}
                dfZaehler = pd.concat([dfZaehler,pd.DataFrame([new_row])], ignore_index=True)
    
    dfNodups = dfStrom.drop_duplicates(['Ort'])
    for index, row in dfNodups.iterrows():
        new_row = {'Nummer': row[2], 'Typ': 'Strom',
                   'Gemeinschaft': 'N', 'Ort': row[0]}
        dfZaehler = pd.concat([dfZaehler,pd.DataFrame([new_row])], ignore_index=True)
    
        
    ## Kosten
    for index, row in dfImportKosten.iterrows():
        new_row = {'Kostenart': row[0], 'Firma': row[1], 'Leistung': row[4],
                   'Betrag(€)': row[3], 'Menge': row[5], 'Einheit': '', 'Jahr': row[6]}
        # print(new_row)
        dfKosten = pd.concat([dfKosten,pd.DataFrame([new_row])], ignore_index=True)
    
    dfKosten.iloc[4, 0] = 'Wartung'
    dfKosten.iloc[5, 0] = 'Wartung'
    dfKosten.iloc[8, 0] = 'Kaltwasser'
    dfKosten.iloc[9, 0] = 'Schmutzwasser'
    dfKosten.iloc[10, 0] = 'Niederschlagswasser'
    dfKosten.iloc[11, 0] = 'Fernwärme'
    dfKosten.iloc[13, 0] = 'Steuer'
    dfKosten.iloc[14, 0] = 'Kabelanschluss'
    dfKosten.iloc[18, 0] = 'Salz'
    dfKosten.iloc[19, 0] = 'Salz'
    
    # Ablesung
    for index, row in dfImportAblesung.iterrows():
        new_row = {'Datum': 2021, 'WEID': row[0], 'Ort': row[1], 'Zählertyp': row[3],
                   'Zählernummer': row[4], 'Anfangsstand': row[6], 'Endstand': row[5]}
        # print(new_row)
        dfAblesung = pd.concat([dfAblesung,pd.DataFrame([new_row])], ignore_index=True)
    
    for index, row in dfStrom.iterrows():
        new_row = {'Datum': 2021, 'WEID': row[1], 'Ort': row[0], 'Zählertyp': 'Strom',
                   'Zählernummer': row[2], 'Anfangsstand': row[3], 'Endstand': row[4]}
        # print(new_row)
        dfAblesung = pd.concat([dfAblesung,pd.DataFrame([new_row])], ignore_index=True)
    
    
    # Verbrauch dfVerbrauch ('WEID',Zählernummer','Typ','Verbrauch','Kosten/Einheit'))
    dfVerbrauch['WEID'] = dfAblesung['WEID']
    dfVerbrauch['Zählernummer'] = dfAblesung['Zählernummer']
    dfVerbrauch['Typ'] = dfAblesung['Zählertyp']
    dfVerbrauch['Verbrauch'] = dfAblesung['Endstand'] - dfAblesung['Anfangsstand']
    
    new_row= {'Bezeichnung': 'VerbrauchKaltwasser', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Kaltwasser', 'Menge'].max()}
    dfBerechnungen= pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'VerbrauchKaltwasserG', 'Wert': dfBerechnungen.query("Bezeichnung == 'VerbrauchKaltwasser'")['Wert'].max()-dfVerbrauch.loc[dfVerbrauch['Typ'] == 'Kaltwasser'].sum()['Verbrauch']}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'VerbrauchWarmwasser', 'Wert': dfVerbrauch.loc[dfVerbrauch['Typ'] == 'Warmwasser'].sum()['Verbrauch']}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'VerbrauchStromG', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Strom']['Menge'].max() - dfVerbrauch.loc[dfVerbrauch['Typ'] == 'Strom']['Verbrauch'].sum()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'WarmwasserFernwärmeMWh', 'Wert': 2*dfBerechnungen.query("Bezeichnung == 'VerbrauchWarmwasser'")['Wert'].max()*(dfKonstanten.loc[dfKonstanten['Konstante'] == 'Temperatur Warmwasser', 'Wert'].max()-10)/1000}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'HeizkostenanteilFW', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Fernwärme', 'Menge'].max() - dfBerechnungen.query("Bezeichnung == 'WarmwasserFernwärmeMWh'")['Wert'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'KostenMWh', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Fernwärme']['Betrag(€)'].max() / dfKosten.loc[dfKosten['Kostenart'] == 'Fernwärme']['Menge'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'KostenEinheitKaltwasser', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Kaltwasser', 'Betrag(€)'].max() / dfKosten.loc[dfKosten['Kostenart'] == 'Kaltwasser', 'Menge'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'KostenEinheitSchmutzwasser', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Schmutzwasser', 'Betrag(€)'].max() / dfKosten.loc[dfKosten['Kostenart'] == 'Schmutzwasser', 'Menge'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'KostenEinheitNiederschlagswasser', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Niederschlagswasser', 'Betrag(€)'].max() / dfKosten.loc[dfKosten['Kostenart'] == 'Niederschlagswasser', 'Menge'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'KaltwasserPreis', 'Wert': dfBerechnungen.query("Bezeichnung =='KostenEinheitKaltwasser'")['Wert'].max()+dfBerechnungen.query("Bezeichnung =='KostenEinheitSchmutzwasser'")['Wert'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'WarmwasserPreis', 'Wert': dfBerechnungen.query("Bezeichnung =='WarmwasserFernwärmeMWh'")['Wert'].max() * dfBerechnungen.query("Bezeichnung =='KostenMWh'")['Wert'].max() / dfBerechnungen.query("Bezeichnung =='VerbrauchWarmwasser'")['Wert'].max() + dfBerechnungen.query("Bezeichnung =='KaltwasserPreis'")['Wert'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'Strompreis', 'Wert': dfKosten.loc[dfKosten['Kostenart'] == 'Strom']['Betrag(€)'].max() / dfKosten.loc[dfKosten['Kostenart'] == 'Strom']['Menge'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    new_row= {'Bezeichnung': 'KostenStromG', 'Wert': dfBerechnungen.query("Bezeichnung =='VerbrauchStromG'")['Wert'].max() * dfBerechnungen.query("Bezeichnung =='Strompreis'")['Wert'].max()}
    dfBerechnungen = pd.concat([dfBerechnungen,pd.DataFrame([new_row])], ignore_index=True)
    
    # Abrechnung erstellen
    dfVerbrauch['Kosten'] = 0
    for index, row in dfVerbrauch.iterrows():
        if dfVerbrauch.loc[index, 'Typ'] == 'Kaltwasser':
            dfVerbrauch.loc[index, 'Kosten'] = dfVerbrauch.loc[index, 'Verbrauch'] * \
                dfBerechnungen.query("Bezeichnung =='KaltwasserPreis'")[
                'Wert'].max()
        elif dfVerbrauch.loc[index, 'Typ'] == 'Strom':
            dfVerbrauch.loc[index, 'Kosten'] = dfVerbrauch.loc[index, 'Verbrauch'] * \
                dfBerechnungen.query("Bezeichnung =='Strompreis'")['Wert'].max()
        elif dfVerbrauch.loc[index, 'Typ'] == 'Warmwasser':
            dfVerbrauch.loc[index, 'Kosten'] = dfVerbrauch.loc[index, 'Verbrauch'] * \
                dfBerechnungen.query("Bezeichnung =='WarmwasserPreis'")[
                'Wert'].max()
    
    dfAbrechnung = pd.DataFrame()
    dfAbrechnung['WEID'] = dfHauptmieter['WEID']
    dfAbrechnung['Mietdauer in Tagen'] = dfHauptmieter['Mietende'].sub(
        dfHauptmieter['Mietbeginn']).mod(365*Day()).dt.days + 1
    dfAbrechnung['Personen'] = dfHauptmieter['Anzahl Personen']
    dfAbrechnung['P*T'] = dfAbrechnung['Mietdauer in Tagen'] * \
        dfAbrechnung['Personen']
    
    grouped = dfVerbrauch.groupby(['WEID', 'Typ'])['Verbrauch', 'Kosten'].sum()
    
    # Eigenanteile
    for index, row in dfAbrechnung.iterrows():
        for name, group in grouped.iterrows():
            if dfAbrechnung.loc[index, 'WEID'] == name[0]:
                if name[1] == 'Kaltwasser':
                    dfAbrechnung.loc[index, 'Kaltwasser m3'] = group[0]
                    dfAbrechnung.loc[index, 'Kaltwasser €'] = group[1]
                elif name[1] == 'Warmwasser':
                    dfAbrechnung.loc[index, 'Warmwasser m3'] = group[0]
                    dfAbrechnung.loc[index, 'Warmwasser €'] = group[1]
                elif name[1] == 'ista':
                    dfAbrechnung.loc[index, 'Verbrauch ista'] = group[0]
                    dfAbrechnung.loc[index, 'ista €'] = group[1]
    # Gemeinschaftsanteile
    for index, row in dfAbrechnung.iterrows():
        dfAbrechnung.loc[index, 'Schmutzwasser €'] = dfBerechnungen.query("Bezeichnung == 'KostenEinheitSchmutzwasser'")[
            'Wert'].max() * (dfAbrechnung.loc[index, 'Kaltwasser m3'] + dfAbrechnung.loc[index, 'Warmwasser m3'])
        dfAbrechnung.loc[index, 'Kaltwasser Gemeinschaft €'] = (dfBerechnungen.query("Bezeichnung == 'KaltwasserPreis'")['Wert'].max(
        ) * dfBerechnungen.query("Bezeichnung == 'VerbrauchKaltwasserG'")['Wert'].max()) / dfAbrechnung['P*T'].sum() * dfAbrechnung.loc[index, 'P*T']
        dfAbrechnung.loc[index, 'Warmwasser Gemeinschaft €'] = (dfBerechnungen.query("Bezeichnung == 'WarmwasserPreis'")['Wert'].max(
        ) * dfBerechnungen.query("Bezeichnung == 'VerbrauchWarmwasserG'")['Wert'].max()) / dfAbrechnung['P*T'].sum() * dfAbrechnung.loc[index, 'P*T']
        dfAbrechnung.loc[index, 'Schmutzwasser Gemeinschaft €'] = (dfKosten.query("Kostenart == 'Schmutzwasser'")['Betrag(€)'].max(
        ) - dfAbrechnung['Schmutzwasser €'].sum()) / dfAbrechnung['P*T'].sum() * dfAbrechnung.loc[index, 'P*T']
        dfAbrechnung.loc[index, 'Niederschlagswasser Gemeinschaft €'] = dfKosten.query("Kostenart == 'Niederschlagswasser'")[
            'Betrag(€)'].max() / dfAbrechnung['P*T'].sum() * dfAbrechnung.loc[index, 'P*T']
    
    
    dfVerbrauch.groupby(['WEID', 'Typ']).sum()
    
    
    # Vorlage erstellen für Ablesung zum exportieren als Excel
    dfAblesung.groupby(by=['WEID', 'Ort', 'Zählernummer',
                       'Zählertyp'])['Endstand'].sum()

    #Import in sqlite3
    conn = sqlite3.connect('nebenkosten.db')

    dfWohnung.to_sql(name='Wohnung', con=conn)
    dfGemeinschaftsraum.to_sql(name='Gemeinschaftsraum', con=conn)
    dfHauptmieter.to_sql(name='Hauptmieter', con=conn)
    dfZaehler.to_sql(name='Zaehler', con=conn)
    dfZaehlertypen.to_sql(name='Zaehlertypen', con=conn)
    dfKostenarten.to_sql(name='Kostenarten', con=conn)
    dfKosten.to_sql(name='Kosten', con=conn)
    dfEinheiten.to_sql(name='Einheiten', con=conn)
    dfUmlageschluessel.to_sql(name='Umlageschluessel', con=conn)
    dfKonstanten.to_sql(name='Konstanten', con=conn)
    dfAblesung.to_sql(name='Ablesung', con=conn)
    dfVerbrauch.to_sql(name='Verbrauch', con=conn)
    dfBerechnungen.to_sql(name='Berechnungen', con=conn)
    dfZaehlerstand.to_sql(name='Zaehlerstand', con=conn)
    dfKostenhistorie.to_sql(name='Kostenhistorie', con=conn)
        
    conn.commit()
    conn.close()


def main():
    pass
    #impdata()

if __name__ == '__main__':
    main()