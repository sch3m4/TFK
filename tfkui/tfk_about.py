# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Wed Sep 12 01:09:55 2012
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmAbout(object):
    def setupUi(self, frmAbout):
        frmAbout.setObjectName(_fromUtf8("frmAbout"))
        frmAbout.setWindowModality(QtCore.Qt.ApplicationModal)
        frmAbout.resize(302, 206)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imagenes/icono")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmAbout.setWindowIcon(icon)
        self.label = QtGui.QLabel(frmAbout)
        self.label.setGeometry(QtCore.QRect(100, 30, 191, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(frmAbout)
        self.label_2.setGeometry(QtCore.QRect(100, 50, 191, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(frmAbout)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 61, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(frmAbout)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 91, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(frmAbout)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 91, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setFrameShape(QtGui.QFrame.NoFrame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(frmAbout)
        self.label_6.setGeometry(QtCore.QRect(100, 70, 131, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(frmAbout)
        self.label_7.setGeometry(QtCore.QRect(10, 90, 57, 14))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(frmAbout)
        self.label_8.setGeometry(QtCore.QRect(100, 90, 71, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.line = QtGui.QFrame(frmAbout)
        self.line.setGeometry(QtCore.QRect(10, 120, 281, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_9 = QtGui.QLabel(frmAbout)
        self.label_9.setGeometry(QtCore.QRect(10, 140, 281, 61))
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(frmAbout)
        self.label_10.setGeometry(QtCore.QRect(100, 10, 191, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(frmAbout)
        self.label_11.setGeometry(QtCore.QRect(10, 10, 51, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))

        self.retranslateUi(frmAbout)
        QtCore.QMetaObject.connectSlotsByName(frmAbout)

    def retranslateUi(self, frmAbout):
        frmAbout.setWindowTitle(QtGui.QApplication.translate("frmAbout", "About TFK", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmAbout", "Twitter Followers Keeper v1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("frmAbout", "<html><head/><body><p><a href=\"http://sch3m4.github.com/tfk\"><span style=\" text-decoration: underline; color:#0000ff;\">http://sch3m4.github.com/tfk</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("frmAbout", "Project:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("frmAbout", "Project URL:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("frmAbout", "Homepage:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("frmAbout", "<html><head/><body><p><a href=\"http://safetybits.net\"><span style=\" text-decoration: underline; color:#0000ff;\">http://safetybits.net</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("frmAbout", "Twitter:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("frmAbout", "<html><head/><body><p><a href=\"http://twitter.com/sch3m4\"><span style=\" text-decoration: underline; color:#0000ff;\">@sch3m4</span></a></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("frmAbout", "<html><head/><body><p align=\"center\">This tool verifies periodically your twitter<br/>followers and store them, so you can be<br/>notified about new followers and people<br/>who have left to follow you.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("frmAbout", "Chema Garcia (a.k.a. sch3m4)", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("frmAbout", "Author:", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
