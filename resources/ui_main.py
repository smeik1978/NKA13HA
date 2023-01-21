# -*- coding: utf-8 -*-

################################################################################
## User-Interface
##
## Created by: Matthias Müller
##
## 
################################################################################

import re, datetime

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, QDate, Qt)
from PySide6.QtGui import (QAction, QFont)
from PySide6.QtWidgets import (QComboBox, QDialog, QDateEdit,
                               QDialogButtonBox, QGridLayout,
                               QLabel, QLineEdit, QMenu, QMenuBar,
                               QMessageBox, QPushButton, 
                               QStackedWidget, QStatusBar, QTableView,
                               QVBoxLayout, QWidget)

from .modules import PandasModel, sql_insert, sql_update, fetch_db_pd, fetch_data, fetch_data2

class dlg_add_ablesung(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Ablesung hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_ablesung = QLabel("Hinzufügen")
        self.lbl_add_ablesung.setObjectName(u"lbl_add_ablesung")
        layout.addWidget(self.lbl_add_ablesung,0,0)
        self.lbl_datum = QLabel("Datum")
        self.lbl_datum.setObjectName(u"lbl_datum")
        layout.addWidget(self.lbl_datum,1,0)
        self.dt_datum = QDateEdit(self)
        self.dt_datum.setObjectName(u"dt_datum")
        self.dt_datum.setDisplayFormat("dd.MM.yyyy")
        self.dt_datum.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_datum,1,1)
        self.lbl_weid = QLabel("WE-ID")
        self.lbl_weid.setObjectName(u"lbl_weid")
        layout.addWidget(self.lbl_weid,2,0)
        self.cmb_weid = QComboBox(self)
        self.cmb_weid.setObjectName(u"cmb_weid")
        self.cmb_weid.setEditable(False)
        self.cmb_weid.currentIndexChanged.connect(self.updateComboWEID)
        layout.addWidget(self.cmb_weid,2,1)
        self.lbl_wohnung = QLabel("Wohnung")
        self.lbl_wohnung.setObjectName(u"lbl_wohnung")
        layout.addWidget(self.lbl_wohnung,3,0)
        self.cmb_wohnung = QComboBox(self)
        self.cmb_wohnung.setObjectName(u"cmb_wohnung")
        self.cmb_wohnung.setEditable(False)
        layout.addWidget(self.cmb_wohnung,3,1)
        self.lbl_ort = QLabel("Ort")
        self.lbl_ort.setObjectName(u"lbl_ort")
        layout.addWidget(self.lbl_ort,4,0)
        self.cmb_ort = QComboBox(self)
        self.cmb_ort.setObjectName(u"cmb_ort")
        self.cmb_ort.setEditable(False)
        layout.addWidget(self.cmb_ort,4,1)        
        self.lbl_typ = QLabel("Typ")
        self.lbl_typ.setObjectName(u"lbl_typ")
        layout.addWidget(self.lbl_typ,5,0)
        self.cmb_typ = QComboBox(self)
        self.cmb_typ.setObjectName(u"cmb_typ")
        self.cmb_typ.setEditable(False)
        layout.addWidget(self.cmb_typ,5,1)
        self.lbl_nummer = QLabel("Nummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,6,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(False)
        layout.addWidget(self.cmb_nummer,6,1)
        self.lbl_anfang = QLabel("Anfangsstand")
        self.lbl_anfang.setObjectName(u"lbl_anfang")
        layout.addWidget(self.lbl_anfang,7,0)
        self.cmb_anfang = QComboBox(self)
        self.cmb_anfang.setObjectName(u"cmb_anfang")
        self.cmb_anfang.setEditable(True)
        layout.addWidget(self.cmb_anfang,7,1)
        self.lbl_ende = QLabel("Endstand")
        self.lbl_ende.setObjectName(u"lbl_ende")
        layout.addWidget(self.lbl_ende,8,0)
        self.cmb_ende = QComboBox(self)
        self.cmb_ende.setObjectName(u"cmb_ende")
        self.cmb_ende.setEditable(True)
        layout.addWidget(self.cmb_ende,8,1)
        self.setLayout(layout)
        
        #pdData = fetch_db_pd('Zaehler')
        #for i, row in pdData.iterrows():
        #    self.cmb_nummer.addItem(str(row[1]))
        #    self.cmb_typ.addItem(str(row[2]))
        #    self.cmb_ort.addItem(str(row[4]))
        pdData = fetch_db_pd('Vermietung')
        pdData = pdData.sort_values('WEID')
        for i, row in pdData.iterrows():
            self.cmb_weid.addItem(str(row[1]))     
           
    # Combo füllen
    def updateComboWEID(self):
        self.cmb_wohnung.clear()
        self.cmb_nummer.clear()
        self.cmb_typ.clear()
        weid = str(self.cmb_weid.currentText())
        wohnung = fetch_data2('Vermietung', 'WEID', weid)
        #print(value)
        self.cmb_wohnung.addItem(str(wohnung[0][2]))
        zaehler = fetch_db_pd('Zaehler')
        grouped = zaehler.groupby(by=['Wohnung', 'Typ']).max()
        for name, group in grouped.iterrows():
            if name[0] == str(wohnung[0][2]):
                self.cmb_typ.addItem(name[1])
        grouped = zaehler.groupby(by=['Typ', 'Nummer']).max()
        for name, group in grouped.iterrows():
            if name[0] == 'Heizung':
                if group[2] == str(wohnung[0][2]):
                    self.cmb_nummer.addItem(name[1])

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_zaehler.currentText())
        if valid:
            pdData = fetch_db_pd('Ablesung')
            pdData['Zaehlernummer'] = pdData['Zaehlernummer'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Dieser Zähler wurde schon erfasst.")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_nummer.currentText() in pdData['Zaehlernummer'].values:
                msg_exist()
            else:
                ablesung = (self.dt_datum.date().toString(self.dt_datum.displayFormat()), self.cmb_weid.currentText(), self.cmb_wohnung.currentText(), self.cmb_typ.currentText(),
                            self.cmb_nummer.currentText(), self.cmb_anfang.currentText(), self.cmb_ende.currentText())
                sql_insert('Ablesung',ablesung)
                msg_ok()
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_ablesung(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Ablesung bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_ablesung = QLabel("Bearbeiten")
        self.lbl_edit_ablesung.setObjectName(u"lbl_edit_ablesung")
        layout.addWidget(self.lbl_edit_ablesung,0,0)
        self.lbl_datum = QLabel("Datum")
        self.lbl_datum.setObjectName(u"lbl_datum")
        layout.addWidget(self.lbl_datum,1,0)
        self.dt_datum = QDateEdit(self)
        self.dt_datum.setObjectName(u"dt_datum")
        self.dt_datum.setDisplayFormat("dd.MM.yyyy")
        self.dt_datum.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_datum,1,1)
        self.lbl_weid = QLabel("WE-ID")
        self.lbl_weid.setObjectName(u"lbl_weid")
        layout.addWidget(self.lbl_weid,2,0)
        self.cmb_weid = QComboBox(self)
        self.cmb_weid.setObjectName(u"cmb_weid")
        self.cmb_weid.setEditable(False)
        layout.addWidget(self.cmb_weid,2,1)
        self.lbl_ort = QLabel("Ort")
        self.lbl_ort.setObjectName(u"lbl_ort")
        layout.addWidget(self.lbl_ort,3,0)
        self.cmb_ort = QComboBox(self)
        self.cmb_ort.setObjectName(u"cmb_ort")
        self.cmb_ort.setEditable(False)
        layout.addWidget(self.cmb_ort,3,1)
        self.lbl_typ = QLabel("Typ")
        self.lbl_typ.setObjectName(u"lbl_typ")
        layout.addWidget(self.lbl_typ,4,0)
        self.cmb_typ = QComboBox(self)
        self.cmb_typ.setObjectName(u"cmb_typ")
        self.cmb_typ.setEditable(False)
        layout.addWidget(self.cmb_typ,4,1)
        self.lbl_nummer = QLabel("Nummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,5,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(False)
        layout.addWidget(self.cmb_nummer,5,1)
        self.lbl_anfang = QLabel("Anfangsstand")
        self.lbl_anfang.setObjectName(u"lbl_anfang")
        layout.addWidget(self.lbl_anfang,6,0)
        self.cmb_anfang = QComboBox(self)
        self.cmb_anfang.setObjectName(u"cmb_anfang")
        self.cmb_anfang.setEditable(True)
        layout.addWidget(self.cmb_anfang,6,1)
        self.lbl_ende = QLabel("Endstand")
        self.lbl_ende.setObjectName(u"lbl_ende")
        layout.addWidget(self.lbl_ende,7,0)
        self.cmb_ende = QComboBox(self)
        self.cmb_ende.setObjectName(u"cmb_ende")
        self.cmb_ende.setEditable(True)
        layout.addWidget(self.cmb_ende,7,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Ablesung',id)
        #self.cmb_datum.addItem(str(data[0][1]))
        self.dt_datum.setDate(QDate.fromString(str(data[0][1]),"dd.MM.yyyy"))
        self.cmb_weid.addItem(str(data[0][2]))
        self.cmb_ort.addItem(str(data[0][3]))
        self.cmb_typ.addItem(str(data[0][4]))
        self.cmb_nummer.addItem(str(data[0][5]))
        self.cmb_anfang.addItem(str(data[0][6]))
        self.cmb_ende.addItem(str(data[0][7]))
        

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Ablesung')
            pdData['Zaehlernummer'] = pdData['Zaehlernummer'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Nummer gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_nummer.currentText() in pdData['Zaehlernummer'].values:
                msg_exist()
            else:
                data = fetch_data('Ablesung', x)
                ablesung = (self.dt_datum.date().toString(self.dt_datum.displayFormat()), self.cmb_weid.currentText(), self.cmb_ort.currentText(), self.cmb_typ.currentText(),
                            self.cmb_nummer.currentText(), self.cmb_anfang.currentText(), self.cmb_ende.currentText(), data[0][0])
                sql_update('Ablesung',ablesung)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_einheiten(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Einheiten hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_einheiten = QLabel("Einheiten hinzufügen")
        self.lbl_add_einheiten.setObjectName(u"lbl_add_einheiten")
        layout.addWidget(self.lbl_add_einheiten,0,0)
        self.lbl_einheit = QLabel("Einheit")
        self.lbl_einheit.setObjectName(u"lbl_einheit")
        layout.addWidget(self.lbl_einheit,1,0)
        self.cmb_einheit = QComboBox(self)
        self.cmb_einheit.setObjectName(u"cmb_einheit")
        self.cmb_einheit.setEditable(True)
        layout.addWidget(self.cmb_einheit,1,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Einheiten')
        for i, row in pdData.iterrows():
            self.cmb_einheit.addItem(str(row[1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_einheit.currentText())
        if valid:
            pdData = fetch_db_pd('Einheiten')
            pdData['Einheit'] = pdData['Einheit'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Einheit gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_einheit.currentText() in pdData['Einheit'].values:
                msg_exist()
            else:
                einheit = self.cmb_einheit.currentText()
                einheiten =([einheit]) # <<< Da nur ein Wert an die SQl Funktion übermittelt wird, muss dieser in einer List sein.
                sql_insert('Einheiten',einheiten)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_einheiten(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Einheiten bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_einheiten = QLabel("Einheit bearbeiten")
        self.lbl_edit_einheiten.setObjectName(u"lbl_edit_einheiten")
        layout.addWidget(self.lbl_edit_einheiten,0,0)
        self.lbl_einheit = QLabel("Einheit")
        self.lbl_einheit.setObjectName(u"lbl_einheit")
        layout.addWidget(self.lbl_einheit,1,0)
        self.cmb_einheit = QComboBox(self)
        self.cmb_einheit.setObjectName(u"cmb_einheit")
        self.cmb_einheit.setEditable(True)
        layout.addWidget(self.cmb_einheit,1,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Einheiten',id)
        self.cmb_einheit.addItem(str(data[0][1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Einheiten')
            pdData['Einheit'] = pdData['Einheit'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Einheit gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_einheit.currentText() in pdData['Einheit'].values:
                msg_exist()
            else:
                data = fetch_data('Einheiten', x)
                einheit = self.cmb_einheit.currentText()
                einheiten =(einheit)
                einheiten =(einheiten, data[0][0])
                sql_update('Einheiten',einheiten)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_gemeinschaft(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Gemeinschaftsfläche hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_gemeinschaft = QLabel("Hinzufügen")
        self.lbl_add_gemeinschaft.setObjectName(u"lbl_add_gemeinschaft")
        layout.addWidget(self.lbl_add_gemeinschaft,0,0)
        self.lbl_bezeichnung = QLabel("Bezeichnung")
        self.lbl_bezeichnung.setObjectName(u"lbl_bezeichnung")
        layout.addWidget(self.lbl_bezeichnung,1,0)
        self.cmb_bezeichnung = QComboBox(self)
        self.cmb_bezeichnung.setObjectName(u"cmb_bezeichnung")
        self.cmb_bezeichnung.setEditable(True)
        layout.addWidget(self.cmb_bezeichnung,1,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Gemeinschaftsflaechen')
        for i, row in pdData.iterrows():
            self.cmb_bezeichnung.addItem(str(row[1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_einheit.currentText())
        if valid:
            pdData = fetch_db_pd('Gemeinschaftsflaechen')
            pdData['Bezeichnung'] = pdData['Bezeichnung'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Bezeichnung gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_bezeichnung.currentText() in pdData['Bezeichnung'].values:
                msg_exist()
            else:
                bezeichnung = self.cmb_bezeichnung.currentText()
                gemeinschaft =([bezeichnung]) # <<< Da nur ein Wert an die SQl Funktion übermittelt wird, muss dieser in einer List sein.
                sql_insert('Gemeinschaftsflaechen',gemeinschaft)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_gemeinschaft(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Gemeinschaftsflächen bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_gemeinschaft = QLabel("Bearbeiten")
        self.lbl_edit_gemeinschaft.setObjectName(u"lbl_edit_gemeinschaft")
        layout.addWidget(self.lbl_edit_gemeinschaft,0,0)
        self.lbl_bezeichnung = QLabel("Bezeichnung")
        self.lbl_bezeichnung.setObjectName(u"lbl_bezeichnung")
        layout.addWidget(self.lbl_bezeichnung,1,0)
        self.cmb_bezeichnung = QComboBox(self)
        self.cmb_bezeichnung.setObjectName(u"cmb_bezeichnung")
        self.cmb_bezeichnung.setEditable(True)
        layout.addWidget(self.cmb_bezeichnung,1,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Gemeinschaftsflaechen',id)
        self.cmb_bezeichnung.addItem(str(data[0][1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Gemeinschaftsflaechen')
            pdData['Bezeichnung'] = pdData['Bezeichnung'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Bezeichnung gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_bezeichnung.currentText() in pdData['Bezeichnung'].values:
                msg_exist()
            else:
                data = fetch_data('Gemeinschaftsflaechen', x)
                bezeichnung = self.cmb_bezeichnung.currentText()
                gemeinschaft =(bezeichnung)
                gemeinschaft =(gemeinschaft, data[0][0])
                sql_update('Gemeinschaftsflaechen',gemeinschaft)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_kosten(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Kosten hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_kosten = QLabel("Kosten hinzufügen")
        self.lbl_add_kosten.setObjectName(u"lbl_add_kosten")
        layout.addWidget(self.lbl_add_kosten,0,0)
        self.lbl_datum = QLabel("Datum")
        self.lbl_datum.setObjectName(u"lbl_datum")
        layout.addWidget(self.lbl_datum,1,0)
        self.dt_datum = QDateEdit(self)
        self.dt_datum.setObjectName(u"dt_datum")
        self.dt_datum.setDisplayFormat("dd.MM.yyyy")
        self.dt_datum.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_datum,1,1)
        self.lbl_kostenart = QLabel("Kostenart")
        self.lbl_kostenart.setObjectName(u"lbl_kostenart")
        layout.addWidget(self.lbl_kostenart,2,0)
        self.cmb_kostenart = QComboBox(self)
        self.cmb_kostenart.setObjectName(u"cmb_kostenart")
        self.cmb_kostenart.setEditable(False)
        layout.addWidget(self.cmb_kostenart,2,1)
        self.lbl_firma = QLabel("Firma")
        self.lbl_firma.setObjectName(u"lbl_firma")
        layout.addWidget(self.lbl_firma,3,0)
        self.cmb_firma = QComboBox(self)
        self.cmb_firma.setObjectName(u"cmb_firma")
        self.cmb_firma.setEditable(True)
        layout.addWidget(self.cmb_firma,3,1)
        self.lbl_leistung = QLabel("Leistung")
        self.lbl_leistung.setObjectName(u"lbl_leistung")
        layout.addWidget(self.lbl_leistung,4,0)
        self.cmb_leistung = QComboBox(self)
        self.cmb_leistung.setObjectName(u"cmb_leistung")
        self.cmb_leistung.setEditable(True)
        layout.addWidget(self.cmb_leistung,4,1)
        self.lbl_betrag = QLabel("Betrag")
        self.lbl_betrag.setObjectName(u"lbl_betrag")
        layout.addWidget(self.lbl_betrag,5,0)
        self.cmb_betrag = QComboBox(self)
        self.cmb_betrag.setObjectName(u"cmb_betrag")
        self.cmb_betrag.setEditable(True)
        layout.addWidget(self.cmb_betrag,5,1)
        self.lbl_menge = QLabel("Menge")
        self.lbl_menge.setObjectName(u"lbl_menge")
        layout.addWidget(self.lbl_menge,6,0)
        self.cmb_menge = QComboBox(self)
        self.cmb_menge.setObjectName(u"cmb_menge")
        self.cmb_menge.setEditable(True)
        layout.addWidget(self.cmb_menge,6,1)
        self.lbl_einheit = QLabel("Einheit")
        self.lbl_einheit.setObjectName(u"lbl_einheit")
        layout.addWidget(self.lbl_einheit,7,0)
        self.cmb_einheit = QComboBox(self)
        self.cmb_einheit.setObjectName(u"cmb_einheit")
        self.cmb_einheit.setEditable(False)
        layout.addWidget(self.cmb_einheit,7,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Kostenarten')
        for i, row in pdData.iterrows():
            self.cmb_kostenart.addItem(str(row[1]))
        pdData = fetch_db_pd('Einheiten')
        for i, row in pdData.iterrows():
            self.cmb_einheit.addItem(str(row[1]))     

    def action_ok(self):
        valid = True #re.match(r'^\d{2}\.\d{2}\.\d{4}$', self.cmb_datum.currentText())
        if valid:
            pdData = fetch_db_pd('Kosten')
            pdData['Leistung'] = pdData['Leistung'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese kosten gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_leistung.currentText() in pdData['Leistung'].values:
                msg_exist()
            else:
                kosten = (self.dt_datum.date().toString(self.dt_datum.displayFormat()), self.cmb_kostenart.currentText(), self.cmb_firma.currentText(), self.cmb_leistung.currentText(),
                          self.cmb_betrag.currentText(), self.cmb_menge.currentText(), self.cmb_einheit.currentText())
                sql_insert('Kosten',kosten)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Das Datum muss im Format xx.xx.xxxx ("01.01.2022", "31.12.2025") sein')
            button = dlg.exec_()

class dlg_update_kosten(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Kosten bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_kosten = QLabel("Kosten bearbeiten")
        self.lbl_edit_kosten.setObjectName(u"lbl_edit_kosten")
        layout.addWidget(self.lbl_edit_kosten,0,0)
        self.lbl_datum = QLabel("Datum")
        self.lbl_datum.setObjectName(u"lbl_datum")
        layout.addWidget(self.lbl_datum,1,0)
        self.dt_datum = QDateEdit(self)
        self.dt_datum.setObjectName(u"dt_datum")
        self.dt_datum.setDisplayFormat("dd.MM.yyyy")
        self.dt_datum.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_datum,1,1)
        self.lbl_kostenart = QLabel("Kostenart")
        self.lbl_kostenart.setObjectName(u"lbl_kostenart")
        layout.addWidget(self.lbl_kostenart,2,0)
        self.cmb_kostenart = QComboBox(self)
        self.cmb_kostenart.setObjectName(u"cmb_kostenart")
        self.cmb_kostenart.setEditable(False)
        layout.addWidget(self.cmb_kostenart,2,1)
        self.lbl_firma = QLabel("Firma")
        self.lbl_firma.setObjectName(u"lbl_firma")
        layout.addWidget(self.lbl_firma,3,0)
        self.cmb_firma = QComboBox(self)
        self.cmb_firma.setObjectName(u"cmb_firma")
        self.cmb_firma.setEditable(True)
        layout.addWidget(self.cmb_firma,3,1)
        self.lbl_leistung = QLabel("Leistung")
        self.lbl_leistung.setObjectName(u"lbl_leistung")
        layout.addWidget(self.lbl_leistung,4,0)
        self.cmb_leistung = QComboBox(self)
        self.cmb_leistung.setObjectName(u"cmb_leistung")
        self.cmb_leistung.setEditable(True)
        layout.addWidget(self.cmb_leistung,4,1)
        self.lbl_betrag = QLabel("Betrag")
        self.lbl_betrag.setObjectName(u"lbl_betrag")
        layout.addWidget(self.lbl_betrag,5,0)
        self.cmb_betrag = QComboBox(self)
        self.cmb_betrag.setObjectName(u"cmb_betrag")
        self.cmb_betrag.setEditable(True)
        layout.addWidget(self.cmb_leistung,5,1)
        self.lbl_menge = QLabel("Menge")
        self.lbl_menge.setObjectName(u"lbl_menge")
        layout.addWidget(self.lbl_menge,6,0)
        self.cmb_menge = QComboBox(self)
        self.cmb_menge.setObjectName(u"cmb_menge")
        self.cmb_menge.setEditable(True)
        layout.addWidget(self.cmb_menge,6,1)
        self.lbl_einheit = QLabel("Einheit")
        self.lbl_einheit.setObjectName(u"lbl_einheit")
        layout.addWidget(self.lbl_einheit,7,0)
        self.cmb_einheit = QComboBox(self)
        self.cmb_einheit.setObjectName(u"cmb_einheit")
        self.cmb_einheit.setEditable(False)
        layout.addWidget(self.cmb_einheit,7,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Kosten',id)
        self.cmb_nummer.addItem(str(data[0][1]))
        self.cmb_typ.addItem(str(data[0][2]))
        self.cmb_gemeinschaft.addItem(str(data[0][3]))
        self.cmb_ort.addItem(str(data[0][4]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Kosten')
            pdData['Leistung'] = pdData['Leistung'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diesen kosten gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_nummer.currentText() in pdData['Leistung'].values:
                msg_exist()
            else:
                data = fetch_data('Kosten', x)
                kosten = (self.dt_datum.date().toString(self.dt_datum.displayFormat()), self.cmb_kostenart.currentText(), self.cmb_firma.currentText(), self.cmb_leistung.currentText(),
                          self.cmb_betrag.currentText(), self.cmb_menge.currentText(), self.cmb_einheit.currentText(), data[0][0])
                sql_update('Kosten',kosten)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Das Datum muss im Format xx.xx.xxxx ("01.01.2022", "31.12.2025") sein')
            button = dlg.exec_()

class dlg_add_kostenarten(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Kostenarten hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_kostenarten = QLabel("Kostenarten hinzufügen")
        self.lbl_add_kostenarten.setObjectName(u"lbl_add_kostenarten")
        layout.addWidget(self.lbl_add_kostenarten,0,0)
        self.lbl_kostenart = QLabel("Kostenart")
        self.lbl_kostenart.setObjectName(u"lbl_kostenart")
        layout.addWidget(self.lbl_kostenart,1,0)
        self.cmb_kostenart = QComboBox(self)
        self.cmb_kostenart.setObjectName(u"cmb_kostenart")
        self.cmb_kostenart.setEditable(True)
        layout.addWidget(self.cmb_kostenart,1,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Kostenarten')
        for i, row in pdData.iterrows():
            self.cmb_kostenart.addItem(str(row[1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_kostenart.currentText())
        if valid:
            pdData = fetch_db_pd('Kostenarten')
            pdData['Kostenart'] = pdData['Kostenart'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Kostenart gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_kostenart.currentText() in pdData['Kostenart'].values:
                msg_exist()
            else:
                kostenart = self.cmb_kostenart.currentText()
                kostenarten =([kostenart]) # <<< Da nur ein Wert an die SQl Funktion übermittelt wird, muss dieser in einer List sein.
                sql_insert('Kostenarten',kostenarten)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_kostenarten(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Kostenarten bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_kostenarten = QLabel("Kostenart bearbeiten")
        self.lbl_edit_kostenarten.setObjectName(u"lbl_edit_kostenarten")
        layout.addWidget(self.lbl_edit_kostenarten,0,0)
        self.lbl_kostenart = QLabel("Kostenart")
        self.lbl_kostenart.setObjectName(u"lbl_kostenart")
        layout.addWidget(self.lbl_kostenart,1,0)
        self.cmb_kostenart = QComboBox(self)
        self.cmb_kostenart.setObjectName(u"cmb_kostenart")
        self.cmb_kostenart.setEditable(True)
        layout.addWidget(self.cmb_kostenart,1,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Kostenarten',id)
        self.cmb_kostenart.addItem(str(data[0][1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Kostenarten')
            pdData['Kostenart'] = pdData['Kostenart'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese Kostenart gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_kostenart.currentText() in pdData['Kostenart'].values:
                msg_exist()
            else:
                data = fetch_data('Kostenarten', x)
                kostenart = self.cmb_kostenart.currentText()
                kostenarten =(kostenart)
                kostenarten =(kostenarten, data[0][0])
                sql_update('Kostenarten',kostenarten)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_mieter(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Mieter*in hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_mieter = QLabel("Mieter*in hinzufügen")
        self.lbl_add_mieter.setObjectName(u"lbl_add_mieter")
        layout.addWidget(self.lbl_add_mieter,0,0)
        self.lbl_weid = QLabel("WE-ID")
        self.lbl_weid.setObjectName(u"lbl_weid")
        layout.addWidget(self.lbl_weid,1,0)
        self.cmb_weid = QComboBox(self)
        self.cmb_weid.setObjectName(u"cmb_weid")
        self.cmb_weid.setEditable(True)
        layout.addWidget(self.cmb_weid,1,1)
        self.lbl_nummer = QLabel("Wohnungsnummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,2,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(True)
        layout.addWidget(self.cmb_nummer,2,1)
        self.lbl_vorname = QLabel("Vorname")
        self.lbl_vorname.setObjectName(u"lbl_vorname")
        layout.addWidget(self.lbl_vorname,3,0)
        self.cmb_vorname = QComboBox(self)
        self.cmb_vorname.setObjectName(u"cmb_vorname")
        self.cmb_vorname.setEditable(True)
        layout.addWidget(self.cmb_vorname,3,1)
        self.lbl_name = QLabel("Name")
        self.lbl_name.setObjectName(u"lbl_name")
        layout.addWidget(self.lbl_name,4,0)
        self.cmb_name = QComboBox(self)
        self.cmb_name.setObjectName(u"cmb_name")
        self.cmb_name.setEditable(True)
        layout.addWidget(self.cmb_name,4,1)
        self.lbl_strasse = QLabel("Straße")
        self.lbl_strasse.setObjectName(u"lbl_strasse")
        layout.addWidget(self.lbl_strasse,5,0)
        self.cmb_strasse = QComboBox(self)
        self.cmb_strasse.setObjectName(u"cmb_strasse")
        self.cmb_strasse.setEditable(True)
        layout.addWidget(self.cmb_strasse,5,1)
        self.lbl_hausnummer = QLabel("Hausnummer")
        self.lbl_hausnummer.setObjectName(u"lbl_hausnummer")
        layout.addWidget(self.lbl_hausnummer,6,0)
        self.cmb_hausnummer = QComboBox(self)
        self.cmb_hausnummer.setObjectName(u"cmb_hausnummer")
        self.cmb_hausnummer.setEditable(True)
        layout.addWidget(self.cmb_hausnummer,6,1)
        self.lbl_plz = QLabel("Postleitzahl")
        self.lbl_plz.setObjectName(u"lbl_plz")
        layout.addWidget(self.lbl_plz,7,0)
        self.cmb_plz = QComboBox(self)
        self.cmb_plz.setObjectName(u"cmb_plz")
        self.cmb_plz.setEditable(True)
        layout.addWidget(self.cmb_plz,7,1)
        self.lbl_ort = QLabel("Ort")
        self.lbl_ort.setObjectName(u"lbl_ort")
        layout.addWidget(self.lbl_ort,8,0)
        self.cmb_ort = QComboBox(self)
        self.cmb_ort.setObjectName(u"cmb_ort")
        self.cmb_ort.setEditable(True)
        layout.addWidget(self.cmb_ort,8,1)
        self.lbl_mietbeginn = QLabel("Mietbeginn")
        self.lbl_mietbeginn.setObjectName(u"lbl_mietbeginn")
        layout.addWidget(self.lbl_mietbeginn,9,0)
        self.dt_mietbeginn = QDateEdit(self)
        self.dt_mietbeginn.setObjectName(u"dt_mietbeginn")
        self.dt_mietbeginn.setDisplayFormat("dd.MM.yyyy")
        self.dt_mietbeginn.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_mietbeginn,9,1)
        self.lbl_mietende = QLabel("Mietende")
        self.lbl_mietende.setObjectName(u"lbl_mietende")
        layout.addWidget(self.lbl_mietende,10,0)
        self.dt_mietende = QDateEdit(self)
        self.dt_mietende.setObjectName(u"dt_mietende")
        self.dt_mietende.setDisplayFormat("dd.MM.yyyy")
        self.dt_mietende.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_mietende,10,1)
        self.lbl_personen = QLabel("Anzahl Personen")
        self.lbl_personen.setObjectName(u"lbl_personen")
        layout.addWidget(self.lbl_personen,11,0)
        self.cmb_personen = QComboBox(self)
        self.cmb_personen.setObjectName(u"cmb_personen")
        self.cmb_personen.setEditable(True)
        layout.addWidget(self.cmb_personen,11,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Wohnungen')
        for i, row in pdData.iterrows():
            self.cmb_nummer.addItem(str(row[1]))
        pdData = fetch_db_pd('Vermietung')
        for i, row in pdData.iterrows():
            self.cmb_weid.addItem(str(row[1]))

    def action_ok(self):
        valid = re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Vermietung')
            pdData['WEID'] = pdData['WEID'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Die WE-ID gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_weid.currentText() in pdData['WEID'].values:
                msg_exist()
            else:
                weid, wohnung = self.cmb_weid.currentText(), self.cmb_nummer.currentText()
                vorname, name = self.cmb_vorname.currentText(), self.cmb_name.currentText()
                strasse, hausnummer = self.cmb_strasse.currentText(), self.cmb_hausnummer.currentText()
                plz, ort, mietbeginn = self.cmb_plz.currentText(), self.cmb_ort.currentText(), self.dt_mietbeginn.date().toString(self.dt_mietbeginn.displayFormat())
                mietende, personen = self.dt_mietende.date().toString(self.dt_mietende.displayFormat()), self.cmb_personen.currentText()
                mieter =(weid,wohnung,vorname,name,strasse,hausnummer,plz, ort, mietbeginn, mietende, personen)
                sql_insert('Vermietung',mieter)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_mieter(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Mieter*in bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_mieter = QLabel("Mieter*in bearbeiten")
        self.lbl_add_mieter.setObjectName(u"lbl_add_mieter")
        layout.addWidget(self.lbl_add_mieter,0,0)
        self.lbl_weid = QLabel("WE-ID")
        self.lbl_weid.setObjectName(u"lbl_weid")
        layout.addWidget(self.lbl_weid,1,0)
        self.cmb_weid = QComboBox(self)
        self.cmb_weid.setObjectName(u"cmb_weid")
        self.cmb_weid.setEditable(True)
        layout.addWidget(self.cmb_weid,1,1)
        self.lbl_nummer = QLabel("Wohnungsnummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,2,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(True)
        layout.addWidget(self.cmb_nummer,2,1)
        self.lbl_vorname = QLabel("Vorname")
        self.lbl_vorname.setObjectName(u"lbl_vorname")
        layout.addWidget(self.lbl_vorname,3,0)
        self.cmb_vorname = QComboBox(self)
        self.cmb_vorname.setObjectName(u"cmb_vorname")
        self.cmb_vorname.setEditable(True)
        layout.addWidget(self.cmb_vorname,3,1)
        self.lbl_name = QLabel("Name")
        self.lbl_name.setObjectName(u"lbl_name")
        layout.addWidget(self.lbl_name,4,0)
        self.cmb_name = QComboBox(self)
        self.cmb_name.setObjectName(u"cmb_name")
        self.cmb_name.setEditable(True)
        layout.addWidget(self.cmb_name,4,1)
        self.lbl_strasse = QLabel("Straße")
        self.lbl_strasse.setObjectName(u"lbl_strasse")
        layout.addWidget(self.lbl_strasse,5,0)
        self.cmb_strasse = QComboBox(self)
        self.cmb_strasse.setObjectName(u"cmb_strasse")
        self.cmb_strasse.setEditable(True)
        layout.addWidget(self.cmb_strasse,5,1)
        self.lbl_hausnummer = QLabel("Hausnummer")
        self.lbl_hausnummer.setObjectName(u"lbl_hausnummer")
        layout.addWidget(self.lbl_hausnummer,6,0)
        self.cmb_hausnummer = QComboBox(self)
        self.cmb_hausnummer.setObjectName(u"cmb_hausnummer")
        self.cmb_hausnummer.setEditable(True)
        layout.addWidget(self.cmb_hausnummer,6,1)
        self.lbl_plz = QLabel("Postleitzahl")
        self.lbl_plz.setObjectName(u"lbl_plz")
        layout.addWidget(self.lbl_plz,7,0)
        self.cmb_plz = QComboBox(self)
        self.cmb_plz.setObjectName(u"cmb_plz")
        self.cmb_plz.setEditable(True)
        layout.addWidget(self.cmb_plz,7,1)
        self.lbl_ort = QLabel("Ort")
        self.lbl_ort.setObjectName(u"lbl_ort")
        layout.addWidget(self.lbl_ort,8,0)
        self.cmb_ort = QComboBox(self)
        self.cmb_ort.setObjectName(u"cmb_ort")
        self.cmb_ort.setEditable(True)
        layout.addWidget(self.cmb_ort,8,1)
        self.lbl_mietbeginn = QLabel("Mietbeginn")
        self.lbl_mietbeginn.setObjectName(u"lbl_mietbeginn")
        layout.addWidget(self.lbl_mietbeginn,9,0)
        self.dt_mietbeginn = QDateEdit(self)
        self.dt_mietbeginn.setObjectName(u"dt_mietbeginn")
        self.dt_mietbeginn.setDisplayFormat("dd.MM.yyyy")
        #self.dt_mietbeginn.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_mietbeginn,9,1)
        self.lbl_mietende = QLabel("Mietende")
        self.lbl_mietende.setObjectName(u"lbl_mietende")
        layout.addWidget(self.lbl_mietende,10,0)
        self.dt_mietende = QDateEdit(self)
        self.dt_mietende.setObjectName(u"dt_mietende")
        self.dt_mietende.setDisplayFormat("dd.MM.yyyy")
        #self.dt_mietende.setDate(datetime.datetime.now().date())
        layout.addWidget(self.dt_mietende,10,1)
        self.lbl_personen = QLabel("Anzahl Personen")
        self.lbl_personen.setObjectName(u"lbl_personen")
        layout.addWidget(self.lbl_personen,11,0)
        self.cmb_personen = QComboBox(self)
        self.cmb_personen.setObjectName(u"cmb_personen")
        self.cmb_personen.setEditable(True)
        layout.addWidget(self.cmb_personen,11,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Vermietung',id)
        print(data)
        #self.cmb_id.addItem(str(data[0][0]))
        self.cmb_weid.addItem(str(data[0][1]))
        self.cmb_nummer.addItem(str(data[0][2]))
        self.cmb_vorname.addItem(str(data[0][3]))
        self.cmb_name.addItem(str(data[0][4]))
        self.cmb_strasse.addItem(str(data[0][5]))
        self.cmb_hausnummer.addItem(str(data[0][6]))
        self.cmb_plz.addItem(str(data[0][7]))
        self.cmb_ort.addItem(str(data[0][8]))
        self.dt_mietbeginn.setDate(QDate.fromString(str(data[0][9]),"dd.MM.yyyy"))
        self.dt_mietende.setDate(QDate.fromString(str(data[0][10]),"dd.MM.yyyy"))
        self.cmb_personen.addItem(str(data[0][11]))

    def action_ok(self):
        valid = re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Vermietung')
            pdData['WEID'] = pdData['WEID'].astype(str)
            data = fetch_data('Vermietung',x)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Die WE-ID gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_weid.currentText() != data[0][1] and self.cmb_weid.currentText() in pdData['WEID'].values:
                msg_exist()
            else:
                data = fetch_data('Vermietung', x)
                weid, wohnung = self.cmb_weid.currentText(), self.cmb_nummer.currentText()
                vorname, name = self.cmb_vorname.currentText(), self.cmb_name.currentText()
                strasse, hausnummer = self.cmb_strasse.currentText(), self.cmb_hausnummer.currentText()
                plz, ort, mietbeginn = self.cmb_plz.currentText(), self.cmb_ort.currentText(), self.dt_mietbeginn.date().toString(self.dt_mietbeginn.displayFormat())
                mietende, personen = self.dt_mietende.date().toString(self.dt_mietende.displayFormat()), self.cmb_personen.currentText()
                mieter =(weid,wohnung,vorname,name,strasse,hausnummer,plz, ort, mietbeginn, mietende, personen, data[0][0])
                sql_update('Vermietung',mieter)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_stockwerke(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Stockwerke hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_stockwerke = QLabel("Stockwerke hinzufügen")
        self.lbl_add_stockwerke.setObjectName(u"lbl_add_stockwerke")
        layout.addWidget(self.lbl_add_stockwerke,0,0)
        self.lbl_stockwerk = QLabel("Stockwerk")
        self.lbl_stockwerk.setObjectName(u"lbl_stockwerk")
        layout.addWidget(self.lbl_stockwerk,1,0)
        self.cmb_stockwerk = QComboBox(self)
        self.cmb_stockwerk.setObjectName(u"cmb_stockwerk")
        self.cmb_stockwerk.setEditable(True)
        layout.addWidget(self.cmb_stockwerk,1,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Stockwerke')
        for i, row in pdData.iterrows():
            self.cmb_stockwerk.addItem(str(row[1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_stockwerk.currentText())
        if valid:
            pdData = fetch_db_pd('Stockwerke')
            pdData['Stockwerk'] = pdData['Stockwerk'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Dieses Stockwerk gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_stockwerk.currentText() in pdData['Stockwerk'].values:
                msg_exist()
            else:
                stockwerk = self.cmb_stockwerk.currentText()
                stockwerke =([stockwerk]) # <<< Da nur ein Wert an die SQl Funktion übermittelt wird, muss dieser in einer List sein.
                sql_insert('Stockwerke',stockwerke)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_stockwerke(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Stockwerke bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_stockwerke = QLabel("Stockwerk bearbeiten")
        self.lbl_edit_stockwerke.setObjectName(u"lbl_edit_stockwerke")
        layout.addWidget(self.lbl_edit_stockwerke,0,0)
        self.lbl_stockwerk = QLabel("Stockwerk")
        self.lbl_stockwerk.setObjectName(u"lbl_stockwerk")
        layout.addWidget(self.lbl_stockwerk,1,0)
        self.cmb_stockwerk = QComboBox(self)
        self.cmb_stockwerk.setObjectName(u"cmb_stockwerk")
        self.cmb_stockwerk.setEditable(True)
        layout.addWidget(self.cmb_stockwerk,1,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Stockwerke',id)
        self.cmb_stockwerk.addItem(str(data[0][1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Stockwerke')
            pdData['Stockwerk'] = pdData['Stockwerk'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Dieses Stockwerk gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_stockwerk.currentText() in pdData['Stockwerk'].values:
                msg_exist()
            else:
                data = fetch_data('Stockwerke', x)
                stockwerk = self.cmb_stockwerk.currentText()
                stockwerke =(stockwerk)
                stockwerke =(stockwerke, data[0][0])
                sql_update('Stockwerke',stockwerke)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_umlageschluessel(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Umlageschlüssel hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_schluessel = QLabel("Schlüssel hinzufügen")
        self.lbl_add_schluessel.setObjectName(u"lbl_add_schluessel")
        layout.addWidget(self.lbl_add_schluessel,0,0)
        self.lbl_schluessel = QLabel("schlüssel")
        self.lbl_schluessel.setObjectName(u"lbl_schluessel")
        layout.addWidget(self.lbl_schluessel,1,0)
        self.cmb_schluessel = QComboBox(self)
        self.cmb_schluessel.setObjectName(u"cmb_schluessel")
        self.cmb_schluessel.setEditable(True)
        layout.addWidget(self.cmb_schluessel,1,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Umlageschluessel')
        for i, row in pdData.iterrows():
            self.cmb_schluessel.addItem(str(row[1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_schluessel.currentText())
        if valid:
            pdData = fetch_db_pd('Umlageschluessel')
            pdData['Schluessel'] = pdData['Schluessel'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diesen Schlüssel gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_schluessel.currentText() in pdData['Schluessel'].values:
                msg_exist()
            else:
                schluessel = self.cmb_schluessel.currentText()
                umlageschluessel =([schluessel]) # <<< Da nur ein Wert an die SQl Funktion übermittelt wird, muss dieser in einer List sein.
                sql_insert('Umlageschluessel',umlageschluessel)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_umlageschluessel(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Umlageschlüssel bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_schluessel = QLabel("Schlüssel bearbeiten")
        self.lbl_edit_schluessel.setObjectName(u"lbl_edit_schluessel")
        layout.addWidget(self.lbl_edit_schluessel,0,0)
        self.lbl_schluessel = QLabel("Schlüssel")
        self.lbl_schluessel.setObjectName(u"lbl_schluessel")
        layout.addWidget(self.lbl_schluessel,1,0)
        self.cmb_schluessel = QComboBox(self)
        self.cmb_schluessel.setObjectName(u"cmb_schluessel")
        self.cmb_schluessel.setEditable(True)
        layout.addWidget(self.cmb_schluessel,1,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Umlageschluessel',id)
        self.cmb_schluessel.addItem(str(data[0][1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Umlageschluessel')
            pdData['Schluessel'] = pdData['Schluessel'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diesen Schluessel gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_schluessel.currentText() in pdData['Schluessel'].values:
                msg_exist()
            else:
                data = fetch_data('Umlageschluessel', x)
                schluessel = self.cmb_schluessel.currentText()
                umlageschluessel =(schluessel)
                umlageschluessel =(umlageschluessel, data[0][0])
                sql_update('Umlageschluessel',umlageschluessel)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_wohnung(QDialog):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Neue Wohnung hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,6,1)
        self.lbl_edit_wohnung = QLabel("Wohnung hinzufügen")
        self.lbl_edit_wohnung.setObjectName(u"lbl_edit_wohnung")
        layout.addWidget(self.lbl_edit_wohnung,0,0)
        self.lbl_nummer = QLabel("Nummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,1,0)
        self.lbl_stockwerk = QLabel("Stockwerk")
        self.lbl_stockwerk.setObjectName(u"lbl_stockwerk")
        layout.addWidget(self.lbl_stockwerk,2,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(True)
        layout.addWidget(self.cmb_nummer,1,1)
        self.cmb_stockwerk = QComboBox(self)
        self.cmb_stockwerk.setObjectName(u"cmb_stockwerk")
        self.cmb_stockwerk.setEditable(True)
        layout.addWidget(self.cmb_stockwerk,2,1)
        self.cmb_qm = QComboBox(self)
        self.cmb_qm.setObjectName(u"cmb_qm")
        self.cmb_qm.setEditable(True)
        layout.addWidget(self.cmb_qm,3,1)
        self.lbl_qm = QLabel("Grö0e in qm")
        self.lbl_qm.setObjectName(u"lbl_qm")
        layout.addWidget(self.lbl_qm,3,0)
        self.lbl_zimmer = QLabel("Anzahl Zimmer")
        self.lbl_zimmer.setObjectName(u"lbl_zimmer")
        layout.addWidget(self.lbl_zimmer,4,0)
        self.cmb_zimmer = QComboBox(self)
        self.cmb_zimmer.setObjectName(u"cmb_zimmer")
        self.cmb_zimmer.setEditable(True)
        layout.addWidget(self.cmb_zimmer,4,1)
        
        self.setLayout(layout)
        
        # pdData = fetch_db_pd('Wohnungen')
        # for i, row in pdData.iterrows():
        #     self.cmb_nummer.addItem(str(row[1]))
        pdData = fetch_db_pd('Stockwerke')
        for i, row in pdData.iterrows():
            self.cmb_stockwerk.addItem(str(row[1]))
    
    def action_ok(self):
        valid = re.match(r'^\d{1}\.\d{1}$', self.cmb_nummer.currentText())
        if valid:
            pdData = fetch_db_pd('Wohnungen')
            pdData['Nummer'] = pdData['Nummer'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Die Nummer gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_nummer.currentText() in pdData['Nummer'].values:
                msg_exist()
            else:
                wohnung = (self.cmb_nummer.currentText(), self.cmb_stockwerk.currentText(), self.cmb_qm.currentText(), self.cmb_zimmer.currentText())
                sql_insert('Wohnungen',wohnung)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format x.x ("0.1", "2.4") sein')
            button = dlg.exec_()

class dlg_update_wohnung(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Wohnung bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,6,1)
        self.lbl_edit_wohnung = QLabel("Wohnung bearbeiten")
        self.lbl_edit_wohnung.setObjectName(u"lbl_edit_wohnung")
        layout.addWidget(self.lbl_edit_wohnung,0,0)
        self.lbl_id = QLabel("ID")
        self.lbl_id.setObjectName(u"lbl_id")
        layout.addWidget(self.lbl_id,1,0)
        self.cmb_id = QComboBox(self)
        self.cmb_id.setObjectName(u"cmb_id")
        self.cmb_id.setEditable(False)
        layout.addWidget(self.cmb_id,1,1)
        self.lbl_nummer = QLabel("Nummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,2,0)
        self.lbl_stockwerk = QLabel("Stockwerk")
        self.lbl_stockwerk.setObjectName(u"lbl_stockwerk")
        layout.addWidget(self.lbl_stockwerk,3,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(True)
        layout.addWidget(self.cmb_nummer,2,1)
        self.cmb_stockwerk = QComboBox(self)
        self.cmb_stockwerk.setObjectName(u"cmb_stockwerk")
        self.cmb_stockwerk.setEditable(True)
        layout.addWidget(self.cmb_stockwerk,3,1)
        self.cmb_qm = QComboBox(self)
        self.cmb_qm.setObjectName(u"cmb_qm")
        self.cmb_qm.setEditable(True)
        layout.addWidget(self.cmb_qm,4,1)
        self.lbl_qm = QLabel("Grö0e in qm")
        self.lbl_qm.setObjectName(u"lbl_qm")
        layout.addWidget(self.lbl_qm,4,0)
        self.lbl_zimmer = QLabel("Anzahl Zimmer")
        self.lbl_zimmer.setObjectName(u"lbl_zimmer")
        layout.addWidget(self.lbl_zimmer,5,0)
        self.cmb_zimmer = QComboBox(self)
        self.cmb_zimmer.setObjectName(u"cmb_zimmer")
        self.cmb_zimmer.setEditable(True)
        layout.addWidget(self.cmb_zimmer,5,1)
        self.setLayout(layout)
 
        data = fetch_data('Wohnungen',id)
        self.cmb_id.addItem(str(data[0][0]))
        self.cmb_nummer.addItem(str(data[0][1]))
        self.cmb_stockwerk.addItem(str(data[0][2]))
        self.cmb_qm.addItem(str(data[0][3]))
        self.cmb_zimmer.addItem(str(data[0][4]))
    
    def action_ok(self):
        valid = re.match(r'^\d{1}\.\d{1,2}$', self.cmb_nummer.currentText())
        if valid:          
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde aktualisiert")
                button = dlg.exec_()
            
            wohnung = (self.cmb_nummer.currentText(), self.cmb_stockwerk.currentText(), self.cmb_qm.currentText(), self.cmb_zimmer.currentText(), int(self.cmb_id.currentText()))
            sql_update('Wohnungen',wohnung)
            msg_ok()    
            self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format x.x ("0.1", "2.4") sein')
            button = dlg.exec_()

class frm_neue_wohnung(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neue Wohnung hinzufügen")
        layout = QVBoxLayout()
        self.label = QLabel("Neue Wohnung hinzufügen")
        self.cmb_wohnungen = QComboBox(self)
        self.cmb_wohnungen.setObjectName(u"cmb_wohnungen")
        self.cmb_wohnungen.setGeometry(QRect(10,50,100,30))
        self.lbl_wohnungen_nummer = QLabel("Nummer")
        self.lbl_wohnungen_nummer.setObjectName(u"lbl_wohnungen_nummer")
        self.lbl_wohnungen_nummer.setGeometry(QRect(10, 100, 100, 30))
        self.tbx_wohnungen = QLineEdit(self)
        self.tbx_wohnungen.setObjectName(u"tbx_wohnungen")
        self.tbx_wohnungen.setGeometry(QRect(10,150,100,30))
        
        layout.addWidget(self.label)
        layout.addWidget(self.cmb_wohnungen)
        layout.addWidget(self.lbl_wohnungen_nummer)
        layout.addWidget(self.tbx_wohnungen)
        self.setLayout(layout)

class dlg_add_zaehler(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("zaehler hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_zaehler = QLabel("zaehler hinzufügen")
        self.lbl_add_zaehler.setObjectName(u"lbl_add_zaehler")
        layout.addWidget(self.lbl_add_zaehler,0,0)
        self.lbl_nummer = QLabel("Nummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,1,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(True)
        layout.addWidget(self.cmb_nummer,1,1)
        self.lbl_typ = QLabel("Typ")
        self.lbl_typ.setObjectName(u"lbl_typ")
        layout.addWidget(self.lbl_typ,2,0)
        self.cmb_typ = QComboBox(self)
        self.cmb_typ.setObjectName(u"cmb_typ")
        self.cmb_typ.setEditable(True)
        layout.addWidget(self.cmb_typ,2,1)
        self.lbl_gemeinschaft = QLabel("Gemeinschaft J/N")
        self.lbl_gemeinschaft.setObjectName(u"lbl_gemeinschaft")
        layout.addWidget(self.lbl_gemeinschaft,3,0)
        self.cmb_gemeinschaft = QComboBox(self)
        self.cmb_gemeinschaft.setObjectName(u"cmb_gemeinschaft")
        self.cmb_gemeinschaft.setEditable(True)
        layout.addWidget(self.cmb_gemeinschaft,3,1)
        self.lbl_wohnung = QLabel("Wohnung")
        self.lbl_wohnung.setObjectName(u"lbl_wohnung")
        layout.addWidget(self.lbl_wohnung,4,0)
        self.cmb_wohnung = QComboBox(self)
        self.cmb_wohnung.setObjectName(u"cmb_wohnung")
        self.cmb_wohnung.setEditable(True)
        layout.addWidget(self.cmb_wohnung,4,1)
        self.lbl_ort = QLabel("Ort")
        self.lbl_ort.setObjectName(u"lbl_ort")
        layout.addWidget(self.lbl_ort,5,0)
        self.cmb_ort = QComboBox(self)
        self.cmb_ort.setObjectName(u"cmb_ort")
        self.cmb_ort.setEditable(True)
        layout.addWidget(self.cmb_ort,5,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Zaehlertypen')
        for i, row in pdData.iterrows():
            self.cmb_typ.addItem(str(row[1]))
        if self.cmb_gemeinschaft.currentText() == "J":
            pdData =fetch_db_pd('Gemeinschaftsflaechen')
            for i, row in pdData.iterrows():
                self.cmb_wohnung.addItem(str(row[1]))
        elif self.cmb_gemeinschaft.currentText() == "N":
            pdData = fetch_db_pd('Wohnungen')
            for i, row in pdData.iterrows():
                self.cmb_wohnung.addItem(str(row[1]))     

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_zaehler.currentText())
        if valid:
            pdData = fetch_db_pd('Zaehler')
            pdData['Nummer'] = pdData['Nummer'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diese zaehler gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_nummer.currentText() in pdData['Nummer'].values:
                msg_exist()
            else:
                zaehler = (self.cmb_nummer.currentText(), self.cmb_typ.currentText(), self.cmb_gemeinschaft.currentText(),
                           self.cmb_wohnung.currentText(), self.cmb_ort.currentText())
                sql_insert('Zaehler',zaehler)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_zaehler(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Zähler bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_zaehler = QLabel("Zähler bearbeiten")
        self.lbl_edit_zaehler.setObjectName(u"lbl_edit_zaehler")
        layout.addWidget(self.lbl_edit_zaehler,0,0)
        self.lbl_nummer = QLabel("Nummer")
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        layout.addWidget(self.lbl_nummer,1,0)
        self.cmb_nummer = QComboBox(self)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setEditable(True)
        layout.addWidget(self.cmb_nummer,1,1)
        self.lbl_typ = QLabel("Typ")
        self.lbl_typ.setObjectName(u"lbl_typ")
        layout.addWidget(self.lbl_typ,2,0)
        self.cmb_typ = QComboBox(self)
        self.cmb_typ.setObjectName(u"cmb_typ")
        self.cmb_typ.setEditable(True)
        layout.addWidget(self.cmb_typ,2,1)
        self.lbl_gemeinschaft = QLabel("Gemeinschaft J/N")
        self.lbl_gemeinschaft.setObjectName(u"lbl_gemeinschaft")
        layout.addWidget(self.lbl_gemeinschaft,3,0)
        self.cmb_gemeinschaft = QComboBox(self)
        self.cmb_gemeinschaft.setObjectName(u"cmb_gemeinschaft")
        self.cmb_gemeinschaft.setEditable(True)
        layout.addWidget(self.cmb_gemeinschaft,3,1)
        self.lbl_wohnung = QLabel("Wohnung")
        self.lbl_wohnung.setObjectName(u"lbl_wohnung")
        layout.addWidget(self.lbl_wohnung,4,0)
        self.cmb_wohnung = QComboBox(self)
        self.cmb_wohnung.setObjectName(u"cmb_wohnung")
        self.cmb_wohnung.setEditable(True)
        layout.addWidget(self.cmb_wohnung,4,1)
        self.lbl_ort = QLabel("Ort")
        self.lbl_ort.setObjectName(u"lbl_ort")
        layout.addWidget(self.lbl_ort,5,0)
        self.cmb_ort = QComboBox(self)
        self.cmb_ort.setObjectName(u"cmb_ort")
        self.cmb_ort.setEditable(True)
        layout.addWidget(self.cmb_ort,5,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Zaehler',id)
        self.cmb_nummer.addItem(str(data[0][1]))
        self.cmb_typ.addItem(str(data[0][2]))
        self.cmb_gemeinschaft.addItem(str(data[0][3]))
        self.cmb_wohnung.addItem(str(data[0][4]))
        self.cmb_ort.addItem(str(data[0][5]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Zaehler')
            pdData['Nummer'] = pdData['Nummer'].astype(str)
            data = fetch_data('Zaehler',x)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diesen zaehler gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_nummer.currentText() != data[0][1] and self.cmb_nummer.currentText() in pdData['Nummer'].values:
                msg_exist()
            else:
                data = fetch_data('Zaehler', x)
                zaehler = (self.cmb_nummer.currentText(), self.cmb_typ.currentText(), self.cmb_gemeinschaft.currentText(),
                           self.cmb_wohnung.currentText(), self.cmb_ort.currentText(), data[0][0])
                sql_update('Zaehler',zaehler)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_add_zaehlertypen(QDialog):
    def __init__(self) -> None:
        super().__init__()
        layout = QGridLayout()
        self.setWindowTitle("Zählertypen hinzufügen")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_add_zaehler = QLabel("Zählertyp hinzufügen")
        self.lbl_add_zaehler.setObjectName(u"lbl_add_zaehler")
        layout.addWidget(self.lbl_add_zaehler,0,0)
        self.lbl_zaehler = QLabel("Typ")
        self.lbl_zaehler.setObjectName(u"lbl_zaehler")
        layout.addWidget(self.lbl_zaehler,1,0)
        self.cmb_zaehler = QComboBox(self)
        self.cmb_zaehler.setObjectName(u"cmb_zaehler")
        self.cmb_zaehler.setEditable(True)
        layout.addWidget(self.cmb_zaehler,1,1)
        self.setLayout(layout)
        
        pdData = fetch_db_pd('Zaehlertypen')
        for i, row in pdData.iterrows():
            self.cmb_zaehler.addItem(str(row[1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_zaehler.currentText())
        if valid:
            pdData = fetch_db_pd('Zaehlertypen')
            pdData['Typ'] = pdData['Typ'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diesen Zählertyp gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_zaehler.currentText() in pdData['Typ'].values:
                msg_exist()
            else:
                zaehler = self.cmb_zaehler.currentText()
                zaehler =([zaehler]) # <<< Da nur ein Wert an die SQl Funktion übermittelt wird, muss dieser in einer List sein.
                sql_insert('Zaehlertypen',zaehler)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class dlg_update_zaehlertypen(QDialog):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        layout = QGridLayout()
        self.setWindowTitle("Zählertypen bearbeiten")
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.action_ok)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox,12,1)
        self.lbl_edit_zaehler = QLabel("Bearbeiten")
        self.lbl_edit_zaehler.setObjectName(u"lbl_edit_zaehler")
        layout.addWidget(self.lbl_edit_zaehler,0,0)
        self.lbl_zaehler = QLabel("Typ")
        self.lbl_zaehler.setObjectName(u"lbl_zaehler")
        layout.addWidget(self.lbl_zaehler,1,0)
        self.cmb_zaehler = QComboBox(self)
        self.cmb_zaehler.setObjectName(u"cmb_zaehler")
        self.cmb_zaehler.setEditable(True)
        layout.addWidget(self.cmb_zaehler,1,1)
        self.setLayout(layout)
        
        global x
        x = id              # <<< Wichtig! Leitet die ID weiter an fetch_data n def action_ok
        data = fetch_data('Zaehlertypen',id)
        self.cmb_zaehler.addItem(str(data[0][1]))

    def action_ok(self):
        valid = True #re.match(r"\b\d{5}\b", self.cmb_weid.currentText())
        if valid:
            pdData = fetch_db_pd('Zaehlertypen')
            pdData['Typ'] = pdData['Typ'].astype(str)
                            
            def msg_exist():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Achtung!")
                dlg.setText("Diesen Zählertyp gibt es schon")
                button = dlg.exec_()
                
            def msg_ok():
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Erfolgreich!")
                dlg.setText("Der Datensatz wurde angelegt")
                button = dlg.exec_()
            
            if self.cmb_zaehler.currentText() in pdData['Typ'].values:
                msg_exist()
            else:
                data = fetch_data('Zaehlertypen', x)
                zaehler = self.cmb_zaehler.currentText()
                zaehler =(zaehler)
                zaehler =(zaehler, data[0][0])
                sql_update('Zaehlertypen',zaehler)
                msg_ok()    
                self.accept()
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Achtung!")
            dlg.setText('Die Nummer muss im Format xxxxx ("00101", "00304") sein')
            button = dlg.exec_()

class Ui_frm_main(object):
    def setupUi(self, frm_main):
        if not frm_main.objectName():
            frm_main.setObjectName(u"frm_main")
        frm_main.resize(1000, 600)
        frm_main.setMinimumSize(QSize(1000, 600))
        #frm_main.setMaximumSize(QSize(800, 600))
        self.actionBeenden = QAction(frm_main)
        self.actionBeenden.setObjectName(u"actionBeenden")
        self.actionWohnungen = QAction(frm_main)
        self.actionWohnungen.setObjectName(u"actionWohnungen")
        self.actionvermietung = QAction(frm_main)
        self.actionvermietung.setObjectName(u"mn_vermietung")
        self.actionVorlagen_erstellen = QAction(frm_main)
        self.actionVorlagen_erstellen.setObjectName(u"actionVorlagen_erstellen")
        self.actionImport = QAction(frm_main)
        self.actionImport.setObjectName(u"actionImport")
        self.actionEinheiten = QAction(frm_main)
        self.actionEinheiten.setObjectName(u"actionEinheiten")
        self.actionGemeinschaftsflaechen = QAction(frm_main)
        self.actionGemeinschaftsflaechen.setObjectName(u"actionGemeinschaftsflaechen")
        self.actionKosten = QAction(frm_main)
        self.actionKosten.setObjectName(u"actionKosten")
        self.actionKostenarten = QAction(frm_main)
        self.actionKostenarten.setObjectName(u"actionKostenarten")
        self.actionUmlageschluessel = QAction(frm_main)
        self.actionUmlageschluessel.setObjectName(u"actionUmlageschluessel")
        self.actionStockwerke = QAction(frm_main)
        self.actionStockwerke.setObjectName(u'actionStockwerke')
        self.actionZaehler = QAction(frm_main)
        self.actionZaehler.setObjectName(u"actionZaehler")
        self.actionZaehlertypen = QAction(frm_main)
        self.actionZaehlertypen.setObjectName(u"actionZaehlertypen")
        self.actionAblesung = QAction(frm_main)
        self.actionAblesung.setObjectName(u"actionAblesung")
        self.actionVermietung = QAction(frm_main)
        self.actionVermietung.setObjectName(u"actionVermietung")
        self.actionVerbrauch = QAction(frm_main)
        self.actionVerbrauch.setObjectName(u"actionVerbrauch")
        self.centralwidget = QWidget(frm_main)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.p_main = QWidget()
        self.p_main.setObjectName(u"p_main")
        self.lbl_main = QLabel(self.p_main)
        self.lbl_main.setObjectName(u"lbl_main")
        self.lbl_main.setGeometry(QRect(0, 0, 780, 20))
        font = QFont()
        font.setPointSize(14)
        self.lbl_main.setFont(font)
        self.lbl_main.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.p_main)
        
        self.p_ablesung = QWidget()
        self.p_ablesung.setObjectName(u"p_ablesung")
        self.lbl_ablesung = QLabel(self.p_ablesung)
        self.lbl_ablesung.setObjectName(u"lbl_ablesung")
        self.lbl_ablesung.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_ablesung.setFont(font)
        self.lbl_ablesung.setAlignment(Qt.AlignCenter)
        self.tbl_ablesung = QTableView(self.p_ablesung)
        self.tbl_ablesung.setObjectName(u"tbl_ablesung")
        self.tbl_ablesung.setGeometry(QRect(10, 30, 950, 400))
        self.btn_ablesung_add = QPushButton(self.p_ablesung)
        self.btn_ablesung_add.setObjectName(u"btn_ablesung_add")
        self.btn_ablesung_add.setGeometry(QRect(50,450,150,25))
        self.btn_ablesung_edit = QPushButton(self.p_ablesung)
        self.btn_ablesung_edit.setObjectName(u"btn_ablesung_edit")
        self.btn_ablesung_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_ablesung)
        
        self.p_einheiten = QWidget()
        self.p_einheiten.setObjectName(u"p_einheiten")
        self.lbl_einheiten = QLabel(self.p_einheiten)
        self.lbl_einheiten.setObjectName(u"lbl_einheiten")
        self.lbl_einheiten.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_einheiten.setFont(font)
        self.lbl_einheiten.setAlignment(Qt.AlignCenter)
        self.tbl_einheiten = QTableView(self.p_einheiten)
        self.tbl_einheiten.setObjectName(u"tbl_einheiten")
        self.tbl_einheiten.setGeometry(QRect(10, 30, 950, 400))
        self.btn_einheiten_add = QPushButton(self.p_einheiten)
        self.btn_einheiten_add.setObjectName(u"btn_einheiten_add")
        self.btn_einheiten_add.setGeometry(QRect(50,450,150,25))
        self.btn_einheiten_edit = QPushButton(self.p_einheiten)
        self.btn_einheiten_edit.setObjectName(u"btn_einheiten_edit")
        self.btn_einheiten_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_einheiten)
        
        self.p_gemeinschaft = QWidget()
        self.p_gemeinschaft.setObjectName(u"p_gemeinschaft")
        self.tbl_gemeinschaft = QTableView(self.p_gemeinschaft)
        self.tbl_gemeinschaft.setObjectName(u"tbl_gemeinschaft")
        self.tbl_gemeinschaft.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_gemeinschaft = QLabel(self.p_gemeinschaft)
        self.lbl_gemeinschaft.setObjectName(u"lbl_gemeinschaft")
        self.lbl_gemeinschaft.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_gemeinschaft.setFont(font)
        self.lbl_gemeinschaft.setAlignment(Qt.AlignCenter)
        self.btn_gemeinschaft_add = QPushButton(self.p_gemeinschaft)
        self.btn_gemeinschaft_add.setObjectName(u"btn_gemeinschaft_add")
        self.btn_gemeinschaft_add.setGeometry(QRect(50,450,150,25))
        self.btn_gemeinschaft_edit = QPushButton(self.p_gemeinschaft)
        self.btn_gemeinschaft_edit.setObjectName(u"btn_gemeinschaft_edit")
        self.btn_gemeinschaft_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_gemeinschaft)

        self.p_kosten = QWidget()
        self.p_kosten.setObjectName(u"p_kosten")
        self.lbl_kosten = QLabel(self.p_kosten)
        self.lbl_kosten.setObjectName(u"lbl_kosten")
        self.lbl_kosten.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_kosten.setFont(font)
        self.lbl_kosten.setAlignment(Qt.AlignCenter)
        self.tbl_kosten = QTableView(self.p_kosten)
        self.tbl_kosten.setObjectName(u"tbl_kosten")
        self.tbl_kosten.setGeometry(QRect(10, 30, 950, 400))
        self.btn_kosten_add = QPushButton(self.p_kosten)
        self.btn_kosten_add.setObjectName(u"btn_kosten_add")
        self.btn_kosten_add.setGeometry(QRect(50,450,150,25))
        self.btn_kosten_edit = QPushButton(self.p_kosten)
        self.btn_kosten_edit.setObjectName(u"btn_kosten_edit")
        self.btn_kosten_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_kosten)

        self.p_kostenarten = QWidget()
        self.p_kostenarten.setObjectName(u"p_kostenarten")
        self.lbl_kostenarten = QLabel(self.p_kostenarten)
        self.lbl_kostenarten.setObjectName(u"lbl_kostenarten")
        self.lbl_kostenarten.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_kostenarten.setFont(font)
        self.lbl_kostenarten.setAlignment(Qt.AlignCenter)
        self.tbl_kostenarten = QTableView(self.p_kostenarten)
        self.tbl_kostenarten.setObjectName(u"tbl_kostenarten")
        self.tbl_kostenarten.setGeometry(QRect(10, 30, 950, 400))
        self.btn_kostenarten_add = QPushButton(self.p_kostenarten)
        self.btn_kostenarten_add.setObjectName(u"btn_kostenarten_add")
        self.btn_kostenarten_add.setGeometry(QRect(50,450,150,25))
        self.btn_kostenarten_edit = QPushButton(self.p_kostenarten)
        self.btn_kostenarten_edit.setObjectName(u"btn_kostenarten_edit")
        self.btn_kostenarten_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_kostenarten)

        self.p_umlageschluessel = QWidget()
        self.p_umlageschluessel.setObjectName(u"p_umlageschluessel")
        self.tbl_umlageschluessel = QTableView(self.p_umlageschluessel)
        self.tbl_umlageschluessel.setObjectName(u"tbl_umlageschluessel")
        self.tbl_umlageschluessel.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_umlageschluessel = QLabel(self.p_umlageschluessel)
        self.lbl_umlageschluessel.setObjectName(u"lbl_umlageschluessel")
        self.lbl_umlageschluessel.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_umlageschluessel.setFont(font)
        self.lbl_umlageschluessel.setAlignment(Qt.AlignCenter)
        self.btn_umlageschluessel_add = QPushButton(self.p_umlageschluessel)
        self.btn_umlageschluessel_add.setObjectName(u"btn_umlageschluessel_add")
        self.btn_umlageschluessel_add.setGeometry(QRect(50,450,150,25))
        self.btn_umlageschluessel_edit = QPushButton(self.p_umlageschluessel)
        self.btn_umlageschluessel_edit.setObjectName(u"btn_umlageschluessel_edit")
        self.btn_umlageschluessel_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_umlageschluessel)
        
        self.p_stockwerke = QWidget()
        self.p_stockwerke.setObjectName(u"p_stockwerke")
        self.tbl_stockwerke = QTableView(self.p_stockwerke)
        self.tbl_stockwerke.setObjectName(u"tbl_stockwerke")
        self.tbl_stockwerke.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_stockwerke = QLabel(self.p_stockwerke)
        self.lbl_stockwerke.setObjectName(u"lbl_stockwerke")
        self.lbl_stockwerke.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_stockwerke.setFont(font)
        self.lbl_stockwerke.setAlignment(Qt.AlignCenter)
        self.btn_stockwerke_add = QPushButton(self.p_stockwerke)
        self.btn_stockwerke_add.setObjectName(u"btn_stockwerke_add")
        self.btn_stockwerke_add.setGeometry(QRect(50,450,150,25))
        self.btn_stockwerke_edit = QPushButton(self.p_stockwerke)
        self.btn_stockwerke_edit.setObjectName(u"btn_stockwerke_edit")
        self.btn_stockwerke_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_stockwerke)
        
        self.p_verbrauch = QWidget()
        self.p_verbrauch.setObjectName(u"p_verbrauch")
        self.tbl_verbrauch = QTableView(self.p_verbrauch)
        self.tbl_verbrauch.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_verbrauch = QLabel(self.p_verbrauch)
        self.lbl_verbrauch.setObjectName(u"lbl_verbrauch")
        self.lbl_verbrauch.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_verbrauch.setFont(font)
        self.lbl_verbrauch.setAlignment(Qt.AlignCenter)
        self.stackedWidget.addWidget(self.p_verbrauch)
        
        self.p_vermietung = QWidget()
        self.p_vermietung.setObjectName(u"p_vermietung")
        self.tbl_vermietung = QTableView(self.p_vermietung)
        self.tbl_vermietung.setObjectName(u"tbl_vermietung")
        self.tbl_vermietung.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_vermietung = QLabel(self.p_vermietung)
        self.lbl_vermietung.setObjectName(u"lbl_vermietung")
        self.lbl_vermietung.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_vermietung.setFont(font)
        self.lbl_vermietung.setAlignment(Qt.AlignCenter)
        self.btn_vermietung_add = QPushButton(self.p_vermietung)
        self.btn_vermietung_add.setObjectName(u"btn_vermietung_add")
        self.btn_vermietung_add.setGeometry(QRect(50,450,150,25))
        self.btn_vermietung_edit = QPushButton(self.p_vermietung)
        self.btn_vermietung_edit.setObjectName(u"btn_vermietung_edit")
        self.btn_vermietung_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_vermietung)

        self.p_wohnungen = QWidget()
        self.p_wohnungen.setObjectName(u"p_wohnungen")
        self.tbl_wohnungen = QTableView(self.p_wohnungen)
        self.tbl_wohnungen.setObjectName(u"tbl_wohnungen")
        self.tbl_wohnungen.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_wohnungen = QLabel(self.p_wohnungen)
        self.lbl_wohnungen.setObjectName(u"lbl_wohnungen")
        self.lbl_wohnungen.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_wohnungen.setFont(font)
        self.lbl_wohnungen.setAlignment(Qt.AlignCenter)
        self.btn_wohnungen_add = QPushButton(self.p_wohnungen)
        self.btn_wohnungen_add.setObjectName(u"btn_wohnungen_add")
        self.btn_wohnungen_add.setGeometry(QRect(50,450,150,25))
        self.btn_wohnungen_edit =QPushButton(self.p_wohnungen)
        self.btn_wohnungen_edit.setObjectName(u'btn_test')
        self.btn_wohnungen_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_wohnungen)
         
        self.p_zaehler = QWidget()
        self.p_zaehler.setObjectName(u"p_zaehler")
        self.tbl_zaehler = QTableView(self.p_zaehler)
        self.tbl_zaehler.setObjectName(u"tbl_zaehler")
        self.tbl_zaehler.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_zaehler = QLabel(self.p_zaehler)
        self.lbl_zaehler.setObjectName(u"lbl_zaehler")
        self.lbl_zaehler.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_zaehler.setFont(font)
        self.lbl_zaehler.setAlignment(Qt.AlignCenter)
        self.btn_zaehler_add = QPushButton(self.p_zaehler)
        self.btn_zaehler_add.setObjectName(u"btn_zaehler_add")
        self.btn_zaehler_add.setGeometry(QRect(50,450,150,25))
        self.btn_zaehler_edit = QPushButton(self.p_zaehler)
        self.btn_zaehler_edit.setObjectName(u"btn_zaehler_edit")
        self.btn_zaehler_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_zaehler)

        self.p_zaehlertypen = QWidget()
        self.p_zaehlertypen.setObjectName(u"p_zaehlertypen")
        self.tbl_zaehlertypen = QTableView(self.p_zaehlertypen)
        self.tbl_zaehlertypen.setObjectName(u"tbl_zaehlertypen")
        self.tbl_zaehlertypen.setGeometry(QRect(10, 30, 950, 400))
        self.lbl_zaehlertypen = QLabel(self.p_zaehlertypen)
        self.lbl_zaehlertypen.setObjectName(u"lbl_zaehlertypen")
        self.lbl_zaehlertypen.setGeometry(QRect(0, 0, 780, 20))
        self.lbl_zaehlertypen.setFont(font)
        self.lbl_zaehlertypen.setAlignment(Qt.AlignCenter)
        self.btn_zaehlertypen_add = QPushButton(self.p_zaehlertypen)
        self.btn_zaehlertypen_add.setObjectName(u"btn_zaehlertypen_add")
        self.btn_zaehlertypen_add.setGeometry(QRect(50,450,150,25))
        self.btn_zaehlertypen_edit = QPushButton(self.p_zaehlertypen)
        self.btn_zaehlertypen_edit.setObjectName(u"btn_zaehlertypen_edit")
        self.btn_zaehlertypen_edit.setGeometry(QRect(250,450,150,25))
        self.stackedWidget.addWidget(self.p_zaehlertypen)
        
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        frm_main.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(frm_main)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menuDatei = QMenu(self.menubar)
        self.menuDatei.setObjectName(u"menuDatei")
        self.menuStammdaten = QMenu(self.menubar)
        self.menuStammdaten.setObjectName(u"menuStammdaten")
        self.menuExtras = QMenu(self.menubar)
        self.menuExtras.setObjectName(u"menuExtras")
        self.menuVerwaltung = QMenu(self.menubar)
        self.menuVerwaltung.setObjectName(u"menuVerwaltung")
        self.menuAuskunft = QMenu(self.menubar)
        self.menuAuskunft.setObjectName(u"menuAuskunft")
        frm_main.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(frm_main)
        self.statusbar.setObjectName(u"statusbar")
        frm_main.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDatei.menuAction())
        self.menubar.addAction(self.menuStammdaten.menuAction())
        self.menubar.addAction(self.menuVerwaltung.menuAction())
        self.menubar.addAction(self.menuAuskunft.menuAction())
        self.menubar.addAction(self.menuExtras.menuAction())
        self.menuDatei.addAction(self.actionBeenden)
        self.menuStammdaten.addAction(self.actionEinheiten)
        self.menuStammdaten.addAction(self.actionGemeinschaftsflaechen)
        self.menuStammdaten.addAction(self.actionKostenarten)
        self.menuStammdaten.addAction(self.actionUmlageschluessel)
        self.menuStammdaten.addAction(self.actionStockwerke)
        self.menuStammdaten.addAction(self.actionWohnungen)
        self.menuStammdaten.addAction(self.actionZaehler)
        self.menuStammdaten.addAction(self.actionZaehlertypen)
        self.menuExtras.addAction(self.actionVorlagen_erstellen)
        self.menuExtras.addAction(self.actionImport)
        self.menuVerwaltung.addAction(self.actionAblesung)
        self.menuVerwaltung.addAction(self.actionKosten)
        self.menuVerwaltung.addAction(self.actionVermietung)
        self.menuAuskunft.addAction(self.actionVerbrauch)

        self.retranslateUi(frm_main)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(frm_main)
    # setupUi

    def retranslateUi(self, frm_main):
        frm_main.setWindowTitle(QCoreApplication.translate("frm_main", u"Hausverwaltung 13ha Freiheit", None))
        self.actionBeenden.setText(QCoreApplication.translate("frm_main", u"Beenden", None))
        self.actionWohnungen.setText(QCoreApplication.translate("frm_main", u"Wohnungen", None))
        self.actionVermietung.setText(QCoreApplication.translate("frm_main", u"Vermietung", None))
        self.actionVorlagen_erstellen.setText(QCoreApplication.translate("frm_main", u"Vorlagen erstellen", None))
        self.actionImport.setText(QCoreApplication.translate("frm_main", u"Import", None))
        self.actionEinheiten.setText(QCoreApplication.translate("frm_main", u"Einheiten", None))
        self.actionGemeinschaftsflaechen.setText(QCoreApplication.translate("frm_main", u"Gemeinschaftsfl\u00e4chen", None))
        self.actionKosten.setText(QCoreApplication.translate("frm_main", u"Kosten", None))
        self.actionKostenarten.setText(QCoreApplication.translate("frm_main", u"Kostenarten", None))
        self.actionUmlageschluessel.setText(QCoreApplication.translate("frm_main", u"Umlageschl\u00fcssel", None))
        self.actionStockwerke.setText(QCoreApplication.translate("frm_main", u"Stockwerke", None))
        self.actionZaehler.setText(QCoreApplication.translate("frm_main", u"Z\u00e4hler", None))
        self.actionZaehlertypen.setText(QCoreApplication.translate("frm_main", u"Z\u00e4hlertypen", None))
        self.actionAblesung.setText(QCoreApplication.translate("frm_main", u"Ablesung", None))
        self.actionVermietung.setText(QCoreApplication.translate("frm_main", u"Vermietung", None))
        self.actionVerbrauch.setText(QCoreApplication.translate("frm_main", u"Verbrauch", None))
        self.lbl_main.setText(QCoreApplication.translate("frm_main", u" ", None))
        self.lbl_ablesung.setText(QCoreApplication.translate("frm_main", u"Ablesung", None))
        self.btn_ablesung_add.setText(QCoreApplication.translate("frm_main",u"Erfassen", None))
        self.btn_ablesung_edit.setText(QCoreApplication.translate("frm_main",u"Bearbeiten", None))
        self.lbl_einheiten.setText(QCoreApplication.translate("frm_main", u"Einheiten", None))
        self.btn_einheiten_add.setText(QCoreApplication.translate("frm_main",u"Neue Einheit", None))
        self.btn_einheiten_edit.setText(QCoreApplication.translate("frm_main",u"Einheit bearbeiten", None))
        self.lbl_gemeinschaft.setText(QCoreApplication.translate("frm_main", u"Gemeinschaftsfl\u00e4chen", None))
        self.btn_gemeinschaft_add.setText(QCoreApplication.translate("frm_main",u"Neu", None))
        self.btn_gemeinschaft_edit.setText(QCoreApplication.translate("frm_main",u"Bearbeiten", None))
        self.lbl_kosten.setText(QCoreApplication.translate("frm_main", u"Kosten", None))
        self.btn_kosten_add.setText(QCoreApplication.translate("frm_main",u"Kosten erfassen", None))
        self.btn_kosten_edit.setText(QCoreApplication.translate("frm_main",u"Kosten bearbeiten", None))
        self.lbl_kostenarten.setText(QCoreApplication.translate("frm_main", u"Kostenarten", None))
        self.btn_kostenarten_add.setText(QCoreApplication.translate("frm_main",u"Neue Kostenart", None))
        self.btn_kostenarten_edit.setText(QCoreApplication.translate("frm_main",u"Kostenart bearbeiten", None))
        self.lbl_umlageschluessel.setText(QCoreApplication.translate("frm_main", u"Umlageschl\u00fcssel", None))
        self.btn_umlageschluessel_add.setText(QCoreApplication.translate("frm_main",u"Neuer Schl\u00fcssel", None))
        self.btn_umlageschluessel_edit.setText(QCoreApplication.translate("frm_main",u"Schl\u00fcssel bearbeiten", None))
        self.lbl_stockwerke.setText(QCoreApplication.translate("frm_main", u"Stockwerke", None))
        self.btn_stockwerke_add.setText(QCoreApplication.translate("frm_main",u"Neues Stockwerk", None))
        self.btn_stockwerke_edit.setText(QCoreApplication.translate("frm_main",u"Stockwerk bearbeiten", None))
        self.lbl_vermietung.setText(QCoreApplication.translate("frm_main", u"Vermietung", None))
        self.btn_vermietung_add.setText(QCoreApplication.translate("frm_main",u"Neue*r Mieter*in", None))
        self.btn_vermietung_edit.setText(QCoreApplication.translate("frm_main", u"Mieter*in bearbeiten",None))
        self.lbl_wohnungen.setText(QCoreApplication.translate("frm_main", u"Wohnungen", None))
        self.btn_wohnungen_add.setText(QCoreApplication.translate("frm_main",u"Neue Wohnung", None))
        self.btn_wohnungen_edit.setText(QCoreApplication.translate("frm_main",u"Wohnung bearbeiten", None))
        self.lbl_zaehler.setText(QCoreApplication.translate("frm_main", u"Z\u00e4hler", None))
        self.btn_zaehler_add.setText(QCoreApplication.translate("frm_main",u"Neuer Z\u00e4hler", None))
        self.btn_zaehler_edit.setText(QCoreApplication.translate("frm_main",u"Z\u00e4hler bearbeiten", None))
        self.lbl_zaehlertypen.setText(QCoreApplication.translate("frm_main", u"Z\u00e4hlertypen", None))
        self.btn_zaehlertypen_add.setText(QCoreApplication.translate("frm_main",u"Neu", None))
        self.btn_zaehlertypen_edit.setText(QCoreApplication.translate("frm_main",u"Bearbeiten", None))
        self.menuDatei.setTitle(QCoreApplication.translate("frm_main", u"Datei", None))
        self.menuStammdaten.setTitle(QCoreApplication.translate("frm_main", u"Stammdaten", None))
        self.menuExtras.setTitle(QCoreApplication.translate("frm_main", u"Extras", None))
        self.menuVerwaltung.setTitle(QCoreApplication.translate("frm_main", u"Verwaltung", None))
        self.menuAuskunft.setTitle(QCoreApplication.translate("frm_main", u"Auskunft", None))
    # retranslateUi

