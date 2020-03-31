# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diangejiUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_diangeji(object):
    def setupUi(self, diangeji):
        diangeji.setObjectName("diangeji")
        diangeji.resize(353, 378)
        self.centralwidget = QtWidgets.QWidget(diangeji)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(41, 28, 258, 271))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pausePushButton = QtWidgets.QPushButton(self.widget)
        self.pausePushButton.setCheckable(True)
        self.pausePushButton.setObjectName("pausePushButton")
        self.horizontalLayout.addWidget(self.pausePushButton)
        self.changeMusicPushButton = QtWidgets.QPushButton(self.widget)
        self.changeMusicPushButton.setObjectName("changeMusicPushButton")
        self.horizontalLayout.addWidget(self.changeMusicPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.listViewLabel = QtWidgets.QLabel(self.widget)
        self.listViewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.listViewLabel.setObjectName("listViewLabel")
        self.gridLayout.addWidget(self.listViewLabel, 1, 0, 1, 1)
        self.musicListView = QtWidgets.QListView(self.widget)
        self.musicListView.setObjectName("musicListView")
        self.gridLayout.addWidget(self.musicListView, 2, 0, 1, 1)
        self.pausePushButton.raise_()
        self.changeMusicPushButton.raise_()
        self.musicListView.raise_()
        self.listViewLabel.raise_()
        self.listViewLabel.raise_()
        diangeji.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(diangeji)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 353, 23))
        self.menubar.setObjectName("menubar")
        diangeji.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(diangeji)
        self.statusbar.setObjectName("statusbar")
        diangeji.setStatusBar(self.statusbar)

        self.retranslateUi(diangeji)
        QtCore.QMetaObject.connectSlotsByName(diangeji)

    def retranslateUi(self, diangeji):
        _translate = QtCore.QCoreApplication.translate
        diangeji.setWindowTitle(_translate("diangeji", "函数的点歌机"))
        self.pausePushButton.setText(_translate("diangeji", "暂停"))
        self.changeMusicPushButton.setText(_translate("diangeji", "切歌"))
        self.listViewLabel.setText(_translate("diangeji", "点歌列表"))
