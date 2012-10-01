# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loghistory.ui'
#
# Created: Mon Oct  1 23:08:03 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmLog(object):
    def setupUi(self, frmLog):
        frmLog.setObjectName(_fromUtf8("frmLog"))
        frmLog.setWindowModality(QtCore.Qt.ApplicationModal)
        frmLog.resize(600, 369)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imagenes/icono")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmLog.setWindowIcon(icon)
        self.label = QtGui.QLabel(frmLog)
        self.label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnRemoveLog = QtGui.QPushButton(frmLog)
        self.btnRemoveLog.setGeometry(QtCore.QRect(10, 320, 581, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imagenes/imagenes/remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnRemoveLog.setIcon(icon1)
        self.btnRemoveLog.setObjectName(_fromUtf8("btnRemoveLog"))
        self.tblLog = QtGui.QTableWidget(frmLog)
        self.tblLog.setGeometry(QtCore.QRect(10, 30, 581, 281))
        self.tblLog.setAlternatingRowColors(True)
        self.tblLog.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tblLog.setObjectName(_fromUtf8("tblLog"))
        self.tblLog.setColumnCount(0)
        self.tblLog.setRowCount(0)
        self.tblLog.horizontalHeader().setVisible(False)
        self.tblLog.verticalHeader().setVisible(False)

        self.retranslateUi(frmLog)
        QtCore.QMetaObject.connectSlotsByName(frmLog)

    def retranslateUi(self, frmLog):
        frmLog.setWindowTitle(QtGui.QApplication.translate("frmLog", "Log History", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmLog", "Log History:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemoveLog.setText(QtGui.QApplication.translate("frmLog", "Remove Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.tblLog.setSortingEnabled(False)

import resources_rc
