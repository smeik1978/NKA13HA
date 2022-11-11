# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_edit_wohnung.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QMainWindow,
    QSizePolicy, QWidget)

class frm_edit_wohnung(QMainWindow):
    def setupUi(self):
        super(frm_edit_wohnung, self).__init__()
        # if not self.objectName():
        #     self.setObjectName(u"frm_edit_wohnung")
        self.resize(242, 242)
        self.setWindowTitle("Wohnung bearbeiten")
        layout = QGridLayout()
        self.btn_cancel = QPushButton(frm_edit_wohnung)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setGeometry(QRect(120, 200, 83, 24))
        self.btn_ok = QPushButton(frm_edit_wohnung)
        self.btn_ok.setObjectName(u"btn_ok")
        self.btn_ok.setGeometry(QRect(30, 200, 83, 24))
        self.lbl_edit_wohnung = QLabel(frm_edit_wohnung)
        self.lbl_edit_wohnung.setObjectName(u"lbl_edit_wohnung")
        self.lbl_edit_wohnung.setGeometry(QRect(10, 20, 221, 16))
        layout.addWidget(self.lbl_edit_wohnung,0,0)
        self.lbl_nummer = QLabel(frm_edit_wohnung)
        self.lbl_nummer.setObjectName(u"lbl_nummer")
        self.lbl_nummer.setGeometry(QRect(10, 70, 131, 20))
        layout.addWidget(self.lbl_nummer,1,0)
        self.lbl_stockwerk = QLabel(frm_edit_wohnung)
        self.lbl_stockwerk.setObjectName(u"lbl_stockwerk")
        self.lbl_stockwerk.setGeometry(QRect(11, 100, 131, 20))
        self.cmb_nummer = QComboBox(frm_edit_wohnung)
        self.cmb_nummer.setObjectName(u"cmb_nummer")
        self.cmb_nummer.setGeometry(QRect(140, 70, 86, 24))
        self.cmb_nummer.setEditable(True)
        self.cmb_stockwerk = QComboBox(frm_edit_wohnung)
        self.cmb_stockwerk.setObjectName(u"cmb_stockwerk")
        self.cmb_stockwerk.setGeometry(QRect(140, 100, 86, 24))
        self.cmb_stockwerk.setEditable(True)
        self.cmb_qm = QComboBox(frm_edit_wohnung)
        self.cmb_qm.setObjectName(u"cmb_qm")
        self.cmb_qm.setGeometry(QRect(139, 130, 86, 24))
        self.cmb_qm.setEditable(True)
        self.lbl_qm = QLabel(frm_edit_wohnung)
        self.lbl_qm.setObjectName(u"lbl_qm")
        self.lbl_qm.setGeometry(QRect(10, 130, 131, 20))
        self.lbl_zimmer = QLabel(frm_edit_wohnung)
        self.lbl_zimmer.setObjectName(u"lbl_zimmer")
        self.lbl_zimmer.setGeometry(QRect(11, 160, 131, 20))
        self.cmb_zimmer = QComboBox(frm_edit_wohnung)
        self.cmb_zimmer.setObjectName(u"cmb_zimmer")
        self.cmb_zimmer.setGeometry(QRect(140, 160, 86, 24))
        self.cmb_zimmer.setEditable(True)

        #self.retranslateUi(self)
        #QMetaObject.connectSlotsByName(self)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    # setupUi

    def retranslateUi(self, frm_edit_wohnung):
        frm_edit_wohnung.setWindowTitle(QCoreApplication.translate("frm_edit_wohnung", u"Wohnung bearbeiten", None))
        self.btn_cancel.setText(QCoreApplication.translate("frm_edit_wohnung", u"Abbrechen", None))
        self.btn_ok.setText(QCoreApplication.translate("frm_edit_wohnung", u"OK", None))
        self.lbl_edit_wohnung.setText(QCoreApplication.translate("frm_edit_wohnung", u"Neue Wohnung oder bearbeiten", None))
        self.lbl_nummer.setText(QCoreApplication.translate("frm_edit_wohnung", u"Nummer (0.1 z.B)", None))
        self.lbl_stockwerk.setText(QCoreApplication.translate("frm_edit_wohnung", u"Stockwerk", None))
        self.lbl_qm.setText(QCoreApplication.translate("frm_edit_wohnung", u"Gr\u00f6\u00dfe in qm", None))
        self.lbl_zimmer.setText(QCoreApplication.translate("frm_edit_wohnung", u"Anzahl Zimmer", None))
    # retranslateUi

