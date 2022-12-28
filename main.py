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

from PySide6.QtWidgets import (QApplication, QMainWindow)

import resources as res


class Frm_main(QMainWindow, res.Ui_frm_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.stackedWidget.setCurrentWidget(self.p_main)
        self.actionAblesung.triggered.connect(self.show_ablesung)
        self.actionEinheiten.triggered.connect(self.show_einheiten)
        self.btn_einheiten_add.clicked.connect(self.btn_einheiten_add_clicked)
        self.btn_einheiten_edit.clicked.connect(self.btn_einheiten_edit_clicked)
        self.actionGemeinschaftsflaechen.triggered.connect(self.show_gemeinschaftsflaechen)
        self.btn_gemeinschaft_add.clicked.connect(self.btn_gemeinschaft_add_clicked)
        self.btn_gemeinschaft_edit.clicked.connect(self.btn_gemeinschaft_edit_clicked)
        self.actionKosten.triggered.connect(self.show_kosten)
        self.btn_kosten_add.clicked.connect(self.btn_kosten_add_clicked)
        self.btn_kosten_edit.clicked.connect(self.btn_kosten_edit_clicked)
        self.actionKostenarten.triggered.connect(self.show_kostenarten)
        self.btn_kostenarten_add.clicked.connect(self.btn_kostenarten_add_clicked)
        self.btn_kostenarten_edit.clicked.connect(self.btn_kostenarten_edit_clicked)
        self.actionStockwerke.triggered.connect(self.show_stockwerke)
        self.btn_stockwerke_add.clicked.connect(self.btn_stockwerke_add_clicked)
        self.btn_stockwerke_edit.clicked.connect(self.btn_stockwerke_edit_clicked)
        self.actionUmlageschluessel.triggered.connect(self.show_umlageschluessel)
        self.btn_umlageschluessel_add.clicked.connect(self.btn_schluessel_add_clicked)
        self.btn_umlageschluessel_edit.clicked.connect(self.btn_schluessel_edit_clicked)
        self.actionVermietung.triggered.connect(self.show_vermietung)
        self.btn_vermietung_add.clicked.connect(self.btn_vermietung_add_clicked)
        self.btn_vermietung_edit.clicked.connect(self.btn_vermietung_edit_clicked)
        self.actionWohnungen.triggered.connect(self.show_wohnung)
        self.btn_wohnungen_add.clicked.connect(self.btn_wohnungen_add_clicked)
        self.btn_wohnungen_edit.clicked.connect(self.btn_wohnungen_edit_clicked)
        self.actionZaehler.triggered.connect(self.show_zaehler)
        self.btn_zaehler_add.clicked.connect(self.btn_zaehler_add_clicked)
        self.btn_zaehler_edit.clicked.connect(self.btn_zaehler_edit_clicked)
        self.actionZaehlertypen.triggered.connect(self.show_zaehlertypen)
        self.btn_zaehlertypen_add.clicked.connect(self.btn_zaehlertypen_add_clicked)
        self.btn_zaehlertypen_edit.clicked.connect(self.btn_zaehlertypen_edit_clicked)
        self.actionBeenden.triggered.connect(self.close)
        
    def btn_einheiten_add_clicked(self, s):
        dlg = res.dlg_add_einheiten()
        if dlg.exec():
            self.show_einheiten()
        else:
            pass
    
    def btn_gemeinschaft_add_clicked(self, s):
        dlg = res.dlg_add_gemeinschaft()
        if dlg.exec():
            self.show_gemeinschaftsflaechen()
        else:
            pass

    def btn_kosten_add_clicked(self, s):
        dlg = res.dlg_add_kosten()
        if dlg.exec():
            self.show_kosten()
        else:
            pass

    def btn_kostenarten_add_clicked(self, s):
        dlg = res.dlg_add_kostenarten()
        if dlg.exec():
            self.show_kostenarten()
        else:
            pass

    def btn_schluessel_add_clicked(self, s):
        dlg = res.dlg_add_umlageschluessel()
        if dlg.exec():
            self.show_umlageschluessel()
        else:
            pass

    def btn_stockwerke_add_clicked(self, s):
        dlg = res.dlg_add_stockwerke()
        if dlg.exec():
            self.show_stockwerke()
        else:
            pass

    def btn_vermietung_add_clicked(self, s):
        dlg = res.dlg_add_mieter()
        if dlg.exec():
            self.show_vermietung()
        else:
            pass
        
    def btn_wohnungen_add_clicked(self, s):
        dlg = res.dlg_add_wohnung()
        if dlg.exec():
            self.show_wohnung()
        else:
            pass
    
    def btn_zaehler_add_clicked(self, s):
        dlg = res.dlg_add_zaehler()
        if dlg.exec():
            self.show_zaehler()
        else:
            pass
    
    def btn_zaehlertypen_add_clicked(self, s):
        dlg = res.dlg_add_zaehlertypen()
        if dlg.exec():
            self.show_zaehlertypen()
        else:
            pass
    
    def btn_einheiten_edit_clicked(self):
            self.stackedWidget.setCurrentWidget(self.p_einheiten)
            model = self.tbl_einheiten.model()
            rows = sorted(set(index.row() for index in
                        self.tbl_einheiten.selectedIndexes()))
            if rows:
                for row in rows:
                    #print('Row %d is selected' % row)
                    id = model.data(model.index(row,0))
                #print(id)
                dlg = res.dlg_update_einheiten(id)
                if dlg.exec():
                    self.show_einheiten()
                else:
                    pass
    
    def btn_gemeinschaft_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_gemeinschaft)
        model = self.tbl_gemeinschaft.model()
        rows = sorted(set(index.row() for index in
                    self.tbl_gemeinschaft.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_gemeinschaft(id)
            if dlg.exec():
                self.show_gemeinschaftsflaechen()
            else:
                pass
    
    def btn_kostenarten_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_kostenarten)
        model = self.tbl_kostenarten.model()
        rows = sorted(set(index.row() for index in
                    self.tbl_kostenarten.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_kostenarten(id)
            if dlg.exec():
                self.show_kostenarten()
            else:
                pass
    
    def btn_kosten_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_kosten)
        model = self.tbl_kosten.model()
        rows = sorted(set(index.row() for index in
                    self.tbl_kosten.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_kosten(id)
            if dlg.exec():
                self.show_kosten()
            else:
                pass
    
    def btn_schluessel_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_umlageschluessel)
        model = self.tbl_umlageschluessel.model()
        rows = sorted(set(index.row() for index in
                    self.tbl_umlageschluessel.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_umlageschluessel(id)
            if dlg.exec():
                self.show_umlageschluessel()
            else:
                pass
    
    def btn_stockwerke_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_stockwerke)
        model = self.tbl_stockwerke.model()
        rows = sorted(set(index.row() for index in
                    self.tbl_stockwerke.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_stockwerke(id)
            if dlg.exec():
                self.show_stockwerke()
            else:
                pass
    
    def btn_vermietung_edit_clicked(self):
            self.stackedWidget.setCurrentWidget(self.p_vermietung)
            model = self.tbl_vermietung.model()
            rows = sorted(set(index.row() for index in
                        self.tbl_vermietung.selectedIndexes()))
            if rows:
                for row in rows:
                    #print('Row %d is selected' % row)
                    id = model.data(model.index(row,0))
                #print(id)
                dlg = res.dlg_update_mieter(id)
                if dlg.exec():
                    self.show_vermietung()
                else:
                    pass
                
    def btn_wohnungen_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_wohnungen)
        model = self.tbl_wohnungen.model()
        rows = sorted(set(index.row() for index in
                      self.tbl_wohnungen.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_wohnung(id)
            if dlg.exec():
                self.show_wohnung()
            else:
                pass
    
    def btn_zaehler_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_zaehler)
        model = self.tbl_zaehler.model()
        rows = sorted(set(index.row() for index in
                      self.tbl_zaehler.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_zaehler(id)
            if dlg.exec():
                self.show_zaehler()
            else:
                pass
    
    def btn_zaehlertypen_edit_clicked(self):
        self.stackedWidget.setCurrentWidget(self.p_zaehlertypen)
        model = self.tbl_zaehlertypen.model()
        rows = sorted(set(index.row() for index in
                      self.tbl_zaehlertypen.selectedIndexes()))
        if rows:
            for row in rows:
                #print('Row %d is selected' % row)
                id = model.data(model.index(row,0))
            #print(id)
            dlg = res.dlg_update_zaehlertypen(id)
            if dlg.exec():
                self.show_zaehlertypen()
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

    def show_kosten(self):
        self.stackedWidget.setCurrentWidget(self.p_kosten)
        model = res.PandasModel(res.fetch_db_pd('Kosten'))
        self.tbl_kosten.setModel(model)
        
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
        model = res.PandasModel(res.fetch_db_pd('Wohnungen'))
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

if __name__ == '__main__':
    main()
    
    
