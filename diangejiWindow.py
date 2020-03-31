from PyQt5.QtCore import *
from PyQt5 import QtCore
from diangejiUI import Ui_diangeji
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListView, QStatusBar
from PyQt5.QtCore import QTimer, QStringListModel
from bilibili import Danmu


class MainWindow(QMainWindow):
    danmu = Danmu()
    tablefreshtimer = QTimer()
    statusTimer = QTimer()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_diangeji()
        self.ui.setupUi(self)

        self.tablefreshtimer.start(300)
        self.tablefreshtimer.timeout.connect(self.update_table)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusTimer.start(300)
        self.statusTimer.timeout.connect(lambda: self.statusBar.showMessage(self.danmu.tip_label['text']))

    @QtCore.pyqtSlot()
    def on_pausePushButton_clicked(self):
        if self.ui.pausePushButton.isChecked():
            self.ui.pausePushButton.setText('继续')
            self.danmu.pause()
        else:
            self.ui.pausePushButton.setText('暂停')
            self.danmu.recover()

    def update_table(self):
        # if self.danmu.song_queue.isEmpty():
        #     return
        musiclist = [item[1] for item in self.danmu.song_queue.data]
        listModel = QStringListModel()
        listModel.setStringList(musiclist)

        self.ui.musicListView.setModel(listModel)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())