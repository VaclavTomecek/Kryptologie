# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ADFGVX_ADFGX.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ADFGVX(object):
    def setupUi(self, ADFGVX):
        ADFGVX.setObjectName("ADFGVX")
        ADFGVX.resize(793, 704)
        self.centralwidget = QtWidgets.QWidget(ADFGVX)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-4, -1, 800, 720))
        self.tabWidget.setStyleSheet("background-color: rgb(33, 33, 33);")
        self.tabWidget.setObjectName("tabWidget")
        self.ADFGVX_2 = QtWidgets.QWidget()
        self.ADFGVX_2.setObjectName("ADFGVX_2")
        self.Zasifrovat_Button = QtWidgets.QPushButton(self.ADFGVX_2)
        self.Zasifrovat_Button.setGeometry(QtCore.QRect(60, 250, 120, 40))
        self.Zasifrovat_Button.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Zasifrovat_Button.setObjectName("Zasifrovat_Button")
        self.Desifrovat_Button = QtWidgets.QPushButton(self.ADFGVX_2)
        self.Desifrovat_Button.setGeometry(QtCore.QRect(620, 250, 120, 40))
        self.Desifrovat_Button.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Desifrovat_Button.setObjectName("Desifrovat_Button")
        self.label = QtWidgets.QLabel(self.ADFGVX_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 41))
        self.label.setStyleSheet("font: 700 20pt \"Segoe UI\";\n"
"color: rgb(221, 241, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.ADFGVX_2)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 200, 41))
        self.label_2.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_2.setObjectName("label_2")
        self.text_pro_sifrovani = QtWidgets.QTextEdit(self.ADFGVX_2)
        self.text_pro_sifrovani.setGeometry(QtCore.QRect(20, 140, 200, 100))
        self.text_pro_sifrovani.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_pro_sifrovani.setObjectName("text_pro_sifrovani")
        self.text_pro_desifrovani = QtWidgets.QTextEdit(self.ADFGVX_2)
        self.text_pro_desifrovani.setGeometry(QtCore.QRect(580, 140, 200, 100))
        self.text_pro_desifrovani.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_pro_desifrovani.setObjectName("text_pro_desifrovani")
        self.label_3 = QtWidgets.QLabel(self.ADFGVX_2)
        self.label_3.setGeometry(QtCore.QRect(580, 90, 200, 41))
        self.label_3.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.ADFGVX_2)
        self.label_4.setGeometry(QtCore.QRect(320, 100, 160, 41))
        self.label_4.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_4.setObjectName("label_4")
        self.text_zasifrovany = QtWidgets.QTextEdit(self.ADFGVX_2)
        self.text_zasifrovany.setGeometry(QtCore.QRect(20, 350, 200, 100))
        self.text_zasifrovany.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_zasifrovany.setObjectName("text_zasifrovany")
        self.text_desifrovany = QtWidgets.QTextEdit(self.ADFGVX_2)
        self.text_desifrovany.setGeometry(QtCore.QRect(580, 350, 200, 100))
        self.text_desifrovany.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_desifrovany.setObjectName("text_desifrovany")
        self.label_5 = QtWidgets.QLabel(self.ADFGVX_2)
        self.label_5.setGeometry(QtCore.QRect(40, 300, 160, 41))
        self.label_5.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.ADFGVX_2)
        self.label_6.setGeometry(QtCore.QRect(600, 300, 160, 41))
        self.label_6.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_6.setObjectName("label_6")
        self.klic = QtWidgets.QLineEdit(self.ADFGVX_2)
        self.klic.setGeometry(QtCore.QRect(300, 50, 200, 24))
        self.klic.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 14pt \"Segoe UI\";")
        self.klic.setText("")
        self.klic.setObjectName("klic")
        self.label_7 = QtWidgets.QLabel(self.ADFGVX_2)
        self.label_7.setGeometry(QtCore.QRect(340, 0, 120, 41))
        self.label_7.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(221, 241, 0);")
        self.label_7.setObjectName("label_7")
        self.tabulka_matice = QtWidgets.QTableWidget(self.ADFGVX_2)
        self.tabulka_matice.setGeometry(QtCore.QRect(260, 140, 281, 211))
        self.tabulka_matice.setMinimumSize(QtCore.QSize(200, 0))
        self.tabulka_matice.setStyleSheet("")
        self.tabulka_matice.setObjectName("tabulka_matice")
        self.tabulka_matice.setColumnCount(6)
        self.tabulka_matice.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice.setHorizontalHeaderItem(5, item)
        self.tabulka_matice.horizontalHeader().setDefaultSectionSize(35)
        self.Prevest_transpozici = QtWidgets.QPushButton(self.ADFGVX_2)
        self.Prevest_transpozici.setGeometry(QtCore.QRect(620, 40, 120, 40))
        self.Prevest_transpozici.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Prevest_transpozici.setObjectName("Prevest_transpozici")
        self.Generace_Matice = QtWidgets.QPushButton(self.ADFGVX_2)
        self.Generace_Matice.setGeometry(QtCore.QRect(320, 360, 150, 40))
        self.Generace_Matice.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Generace_Matice.setObjectName("Generace_Matice")
        self.stahnout_matici = QtWidgets.QPushButton(self.ADFGVX_2)
        self.stahnout_matici.setGeometry(QtCore.QRect(240, 440, 140, 40))
        self.stahnout_matici.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.stahnout_matici.setObjectName("stahnout_matici")
        self.nahrat_matici = QtWidgets.QPushButton(self.ADFGVX_2)
        self.nahrat_matici.setGeometry(QtCore.QRect(420, 440, 140, 40))
        self.nahrat_matici.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.nahrat_matici.setObjectName("nahrat_matici")
        self.tabWidget.addTab(self.ADFGVX_2, "")
        self.ADFGX = QtWidgets.QWidget()
        self.ADFGX.setObjectName("ADFGX")
        self.tabulka_matice_ADFGX = QtWidgets.QTableWidget(self.ADFGX)
        self.tabulka_matice_ADFGX.setGeometry(QtCore.QRect(295, 140, 221, 191))
        self.tabulka_matice_ADFGX.setMinimumSize(QtCore.QSize(200, 0))
        self.tabulka_matice_ADFGX.setStyleSheet("")
        self.tabulka_matice_ADFGX.setObjectName("tabulka_matice_ADFGX")
        self.tabulka_matice_ADFGX.setColumnCount(5)
        self.tabulka_matice_ADFGX.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabulka_matice_ADFGX.setHorizontalHeaderItem(4, item)
        self.tabulka_matice_ADFGX.horizontalHeader().setDefaultSectionSize(35)
        self.label_14 = QtWidgets.QLabel(self.ADFGX)
        self.label_14.setGeometry(QtCore.QRect(320, 100, 160, 41))
        self.label_14.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_14.setObjectName("label_14")
        self.text_pro_sifrovani_ADFGX = QtWidgets.QTextEdit(self.ADFGX)
        self.text_pro_sifrovani_ADFGX.setGeometry(QtCore.QRect(20, 140, 200, 100))
        self.text_pro_sifrovani_ADFGX.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_pro_sifrovani_ADFGX.setObjectName("text_pro_sifrovani_ADFGX")
        self.Prevest_transpozici_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.Prevest_transpozici_ADFGX.setGeometry(QtCore.QRect(620, 40, 120, 40))
        self.Prevest_transpozici_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Prevest_transpozici_ADFGX.setObjectName("Prevest_transpozici_ADFGX")
        self.text_zasifrovany_ADFGX = QtWidgets.QTextEdit(self.ADFGX)
        self.text_zasifrovany_ADFGX.setGeometry(QtCore.QRect(20, 350, 200, 100))
        self.text_zasifrovany_ADFGX.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_zasifrovany_ADFGX.setObjectName("text_zasifrovany_ADFGX")
        self.label_12 = QtWidgets.QLabel(self.ADFGX)
        self.label_12.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.label_12.setStyleSheet("font: 700 20pt \"Segoe UI\";\n"
"color: rgb(221, 241, 0);")
        self.label_12.setObjectName("label_12")
        self.label_9 = QtWidgets.QLabel(self.ADFGX)
        self.label_9.setGeometry(QtCore.QRect(600, 300, 160, 41))
        self.label_9.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_9.setObjectName("label_9")
        self.text_desifrovany_ADFGX = QtWidgets.QTextEdit(self.ADFGX)
        self.text_desifrovany_ADFGX.setGeometry(QtCore.QRect(580, 350, 200, 100))
        self.text_desifrovany_ADFGX.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_desifrovany_ADFGX.setObjectName("text_desifrovany_ADFGX")
        self.label_8 = QtWidgets.QLabel(self.ADFGX)
        self.label_8.setGeometry(QtCore.QRect(20, 90, 200, 41))
        self.label_8.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_8.setObjectName("label_8")
        self.label_11 = QtWidgets.QLabel(self.ADFGX)
        self.label_11.setGeometry(QtCore.QRect(40, 300, 160, 41))
        self.label_11.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_11.setObjectName("label_11")
        self.text_pro_desifrovani_ADFGX = QtWidgets.QTextEdit(self.ADFGX)
        self.text_pro_desifrovani_ADFGX.setGeometry(QtCore.QRect(580, 140, 200, 100))
        self.text_pro_desifrovani_ADFGX.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 11pt \"Segoe UI\";")
        self.text_pro_desifrovani_ADFGX.setObjectName("text_pro_desifrovani_ADFGX")
        self.label_13 = QtWidgets.QLabel(self.ADFGX)
        self.label_13.setGeometry(QtCore.QRect(340, 0, 120, 41))
        self.label_13.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(221, 241, 0);")
        self.label_13.setObjectName("label_13")
        self.Desifrovat_Button_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.Desifrovat_Button_ADFGX.setGeometry(QtCore.QRect(620, 250, 120, 40))
        self.Desifrovat_Button_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Desifrovat_Button_ADFGX.setObjectName("Desifrovat_Button_ADFGX")
        self.label_10 = QtWidgets.QLabel(self.ADFGX)
        self.label_10.setGeometry(QtCore.QRect(580, 90, 200, 41))
        self.label_10.setStyleSheet("font: 700 16pt \"Segoe UI\";\n"
"color: rgb(41, 226, 0);")
        self.label_10.setObjectName("label_10")
        self.Zasifrovat_Button_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.Zasifrovat_Button_ADFGX.setGeometry(QtCore.QRect(60, 250, 120, 40))
        self.Zasifrovat_Button_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Zasifrovat_Button_ADFGX.setObjectName("Zasifrovat_Button_ADFGX")
        self.klic_ADFGX = QtWidgets.QLineEdit(self.ADFGX)
        self.klic_ADFGX.setGeometry(QtCore.QRect(300, 50, 200, 24))
        self.klic_ADFGX.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 14pt \"Segoe UI\";")
        self.klic_ADFGX.setText("")
        self.klic_ADFGX.setObjectName("klic_ADFGX")
        self.stahnout_matici_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.stahnout_matici_ADFGX.setGeometry(QtCore.QRect(250, 410, 140, 40))
        self.stahnout_matici_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.stahnout_matici_ADFGX.setObjectName("stahnout_matici_ADFGX")
        self.nahrat_matici_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.nahrat_matici_ADFGX.setGeometry(QtCore.QRect(410, 410, 140, 40))
        self.nahrat_matici_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.nahrat_matici_ADFGX.setObjectName("nahrat_matici_ADFGX")
        self.Generace_Matice_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.Generace_Matice_ADFGX.setGeometry(QtCore.QRect(330, 340, 150, 40))
        self.Generace_Matice_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.Generace_Matice_ADFGX.setObjectName("Generace_Matice_ADFGX")
        self.ENGLISH_BUTTON_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.ENGLISH_BUTTON_ADFGX.setGeometry(QtCore.QRect(120, 20, 40, 40))
        self.ENGLISH_BUTTON_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.ENGLISH_BUTTON_ADFGX.setObjectName("ENGLISH_BUTTON_ADFGX")
        self.CZECH_BUTTON_ADFGX = QtWidgets.QPushButton(self.ADFGX)
        self.CZECH_BUTTON_ADFGX.setGeometry(QtCore.QRect(170, 20, 40, 40))
        self.CZECH_BUTTON_ADFGX.setStyleSheet("background-color: rgb(66, 66, 66);\n"
"font: 700 12pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")
        self.CZECH_BUTTON_ADFGX.setObjectName("CZECH_BUTTON_ADFGX")
        self.tabWidget.addTab(self.ADFGX, "")
        ADFGVX.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ADFGVX)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 793, 21))
        self.menubar.setObjectName("menubar")
        self.menuADFG_V_X = QtWidgets.QMenu(self.menubar)
        self.menuADFG_V_X.setObjectName("menuADFG_V_X")
        ADFGVX.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ADFGVX)
        self.statusbar.setObjectName("statusbar")
        ADFGVX.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuADFG_V_X.menuAction())

        self.retranslateUi(ADFGVX)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ADFGVX)

    def retranslateUi(self, ADFGVX):
        _translate = QtCore.QCoreApplication.translate
        ADFGVX.setWindowTitle(_translate("ADFGVX", "ADFGVX"))
        self.Zasifrovat_Button.setText(_translate("ADFGVX", "Zašifrovat"))
        self.Desifrovat_Button.setText(_translate("ADFGVX", "Dešifrovat"))
        self.label.setText(_translate("ADFGVX", "ADFG(V)X"))
        self.label_2.setText(_translate("ADFGVX", "Text pro zašifrování"))
        self.label_3.setText(_translate("ADFGVX", "Text pro dešifrování"))
        self.label_4.setText(_translate("ADFGVX", "Šifrovací matice"))
        self.label_5.setText(_translate("ADFGVX", "Zašifrovaný text"))
        self.label_6.setText(_translate("ADFGVX", "Dešifrovaný text"))
        self.label_7.setText(_translate("ADFGVX", "Zadejte klíč"))
        item = self.tabulka_matice.verticalHeaderItem(0)
        item.setText(_translate("ADFGVX", "A"))
        item = self.tabulka_matice.verticalHeaderItem(1)
        item.setText(_translate("ADFGVX", "D"))
        item = self.tabulka_matice.verticalHeaderItem(2)
        item.setText(_translate("ADFGVX", "F"))
        item = self.tabulka_matice.verticalHeaderItem(3)
        item.setText(_translate("ADFGVX", "G"))
        item = self.tabulka_matice.verticalHeaderItem(4)
        item.setText(_translate("ADFGVX", "V"))
        item = self.tabulka_matice.verticalHeaderItem(5)
        item.setText(_translate("ADFGVX", "X"))
        item = self.tabulka_matice.horizontalHeaderItem(0)
        item.setText(_translate("ADFGVX", "A"))
        item = self.tabulka_matice.horizontalHeaderItem(1)
        item.setText(_translate("ADFGVX", "D"))
        item = self.tabulka_matice.horizontalHeaderItem(2)
        item.setText(_translate("ADFGVX", "F"))
        item = self.tabulka_matice.horizontalHeaderItem(3)
        item.setText(_translate("ADFGVX", "G"))
        item = self.tabulka_matice.horizontalHeaderItem(4)
        item.setText(_translate("ADFGVX", "V"))
        item = self.tabulka_matice.horizontalHeaderItem(5)
        item.setText(_translate("ADFGVX", "X"))
        self.Prevest_transpozici.setText(_translate("ADFGVX", "Převést šifru"))
        self.Generace_Matice.setText(_translate("ADFGVX", "Generovat matici"))
        self.stahnout_matici.setText(_translate("ADFGVX", "Stáhnout matici"))
        self.nahrat_matici.setText(_translate("ADFGVX", "Nahrát matici"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ADFGVX_2), _translate("ADFGVX", "ADFG(V)X"))
        item = self.tabulka_matice_ADFGX.verticalHeaderItem(0)
        item.setText(_translate("ADFGVX", "A"))
        item = self.tabulka_matice_ADFGX.verticalHeaderItem(1)
        item.setText(_translate("ADFGVX", "D"))
        item = self.tabulka_matice_ADFGX.verticalHeaderItem(2)
        item.setText(_translate("ADFGVX", "F"))
        item = self.tabulka_matice_ADFGX.verticalHeaderItem(3)
        item.setText(_translate("ADFGVX", "G"))
        item = self.tabulka_matice_ADFGX.verticalHeaderItem(4)
        item.setText(_translate("ADFGVX", "X"))
        item = self.tabulka_matice_ADFGX.horizontalHeaderItem(0)
        item.setText(_translate("ADFGVX", "A"))
        item = self.tabulka_matice_ADFGX.horizontalHeaderItem(1)
        item.setText(_translate("ADFGVX", "D"))
        item = self.tabulka_matice_ADFGX.horizontalHeaderItem(2)
        item.setText(_translate("ADFGVX", "F"))
        item = self.tabulka_matice_ADFGX.horizontalHeaderItem(3)
        item.setText(_translate("ADFGVX", "G"))
        item = self.tabulka_matice_ADFGX.horizontalHeaderItem(4)
        item.setText(_translate("ADFGVX", "X"))
        self.label_14.setText(_translate("ADFGVX", "Šifrovací matice"))
        self.Prevest_transpozici_ADFGX.setText(_translate("ADFGVX", "Převést"))
        self.label_12.setText(_translate("ADFGVX", "ADFGX"))
        self.label_9.setText(_translate("ADFGVX", "Dešifrovaný text"))
        self.label_8.setText(_translate("ADFGVX", "Text pro zašifrování"))
        self.label_11.setText(_translate("ADFGVX", "Zašifrovaný text"))
        self.label_13.setText(_translate("ADFGVX", "Zadejte klíč"))
        self.Desifrovat_Button_ADFGX.setText(_translate("ADFGVX", "Dešifrovat"))
        self.label_10.setText(_translate("ADFGVX", "Text pro dešifrování"))
        self.Zasifrovat_Button_ADFGX.setText(_translate("ADFGVX", "Zašifrovat"))
        self.stahnout_matici_ADFGX.setText(_translate("ADFGVX", "Stáhnout matici"))
        self.nahrat_matici_ADFGX.setText(_translate("ADFGVX", "Nahrát matici"))
        self.Generace_Matice_ADFGX.setText(_translate("ADFGVX", "Generovat matici"))
        self.ENGLISH_BUTTON_ADFGX.setText(_translate("ADFGVX", "EN"))
        self.CZECH_BUTTON_ADFGX.setText(_translate("ADFGVX", "CZ"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ADFGX), _translate("ADFGVX", "ADFGX"))
        self.menuADFG_V_X.setTitle(_translate("ADFGVX", "ADFG(V)X"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ADFGVX = QtWidgets.QMainWindow()
    ui = Ui_ADFGVX()
    ui.setupUi(ADFGVX)
    ADFGVX.show()
    sys.exit(app.exec_())
