#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hausverwaltung für F13 Turley GmbH / 13ha Freiheit
Version: 1.0
Python 3.8+
Date created: 01.11.2022
Date modified: 11.11.2022
"""
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

import resources as res
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout,
                               QWidget)

class Frm_main(QMainWindow, res.Ui_frm_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.stackedWidget.setCurrentWidget(self.p_main)
        self.actionAblesung.triggered.connect(self.show_ablesung)
        self.actionEinheiten.triggered.connect(self.show_einheiten)
        self.actionGemeinschaftsflaechen.triggered.connect(self.show_gemeinschaftsflaechen)
        self.actionKostenarten.triggered.connect(self.show_kostenarten)
        self.actionStockwerke.triggered.connect(self.show_stockwerke)
        self.actionUmlageschluessel.triggered.connect(self.show_umlageschluessel)
        self.actionVermietung.triggered.connect(self.show_vermietung)
        self.btn_vermietung_add.clicked.connect(self.btn_vermietung_add_clicked)
        self.actionWohnungen.triggered.connect(self.show_wohnung)
        self.btn_wohnungen_add.clicked.connect(self.btn_wohnungen_add_clicked)
        self.actionZaehler.triggered.connect(self.show_zaehler)
        self.actionZaehlertypen.triggered.connect(self.show_zaehlertypen)
        self.actionBeenden.triggered.connect(self.close)

    def btn_wohnungen_add_clicked(self, s):
        dlg = res.add_wohnung()
        if dlg.exec():
            self.show_wohnung()
        else:
            pass
    
    def btn_vermietung_add_clicked(self, s):
        dlg = res.add_mieter()
        if dlg.exec():
            self.show_vermietung()
        else:
            pass
    
    def show_new_window(self, checked):
        self._new_Window = res.frm_edit_wohnung()
        self._new_Window.show()
    
    def show_ablesung(self):
        self.stackedWidget.setCurrentWidget(self.p_ablesung)
        model = res.PandasModel(res.fetch_db_pd('Ablesung'))
        self.tbl_ablesung.setModel(model)

    def show_einheiten(self):
        self.stackedWidget.setCurrentWidget(self.p_einheiten)
        model = res.PandasModel(res.fetch_db_pd('Einheiten'))
        self.tbl_einheiten.setModel(model)
    
    def show_gemeinschaftsflaechen(self):
        self.stackedWidget.setCurrentWidget(self.p_gemeinschaft)
        model = res.PandasModel(res.fetch_db_pd('Gemeinschaftsflaechen'))
        self.tbl_gemeinschaft.setModel(model)

    def show_kostenarten(self):
        self.stackedWidget.setCurrentWidget(self.p_kostenarten)
        model = res.PandasModel(res.fetch_db_pd('Kostenarten'))
        self.tbl_kostenarten.setModel(model)

    def show_umlageschluessel(self):
        self.stackedWidget.setCurrentWidget(self.p_umlageschluessel)
        model = res.PandasModel(res.fetch_db_pd('Umlageschluessel'))
        self.tbl_umlageschluessel.setModel(model)

    def show_stockwerke(self):
        self.stackedWidget.setCurrentWidget(self.p_stockwerke)
        model = res.PandasModel(res.fetch_db_pd('Stockwerke'))
        self.tbl_stockwerke.setModel(model)
    
    def show_vermietung(self):
        self.stackedWidget.setCurrentWidget(self.p_vermietung)
        model = res.PandasModel(res.fetch_db_pd('Vermietung'))
        self.tbl_vermietung.setModel(model)

    def show_wohnung(self):
        self.stackedWidget.setCurrentWidget(self.p_wohnungen)
        pdData = res.fetch_db_pd('Wohnungen')
        model = res.PandasModel(pdData[['Nummer', 'Stockwerk', 'qm', 'Zimmer']])
        self.tbl_wohnungen.setModel(model)
        
    def show_zaehler(self):
        self.stackedWidget.setCurrentWidget(self.p_zaehler)
        model = res.PandasModel(res.fetch_db_pd('Zaehler'))
        self.tbl_zaehler.setModel(model)

    def show_zaehlertypen(self):
        self.stackedWidget.setCurrentWidget(self.p_zaehlertypen)
        model = res.PandasModel(res.fetch_db_pd('Zaehlertypen'))
        self.tbl_zaehlertypen.setModel(model)


def main():
    app = QApplication()
    frm_main = Frm_main()
    frm_main.show()
    app.exec()
#    print(fetch_db_pd('Wohnungen'))

if __name__ == '__main__':
    main()
    
    
