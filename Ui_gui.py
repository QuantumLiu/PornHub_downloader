# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\pyprojects\porndownload\gui.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

import requests,traceback
from requests.exceptions import Timeout,HTTPError,ConnectionError
from PyQt5 import QtCore, QtGui, QtWidgets
from get_video import get_video

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_Dialog,self).__init__()
        self.adds,self.infos,self.title=None,None,None
        self.headers={'use-agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        self.proxies={'https': 'https://127.0.0.1:1080','http': 'http://127.0.0.1:1080'}
        self.set_ui()
        self.set_logic()
        
    def set_ui(self):
        self.setObjectName("Dialog")
        self.resize(594, 659)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setSizeGripEnabled(True)
        self.gridLayout_2 = QtWidgets.QGridLayout(self)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lb_cover = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_cover.sizePolicy().hasHeightForWidth())
        self.lb_cover.setSizePolicy(sizePolicy)
        self.lb_cover.setObjectName("lb_cover")
        self.gridLayout_2.addWidget(self.lb_cover, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.le_input = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_input.sizePolicy().hasHeightForWidth())
        self.le_input.setSizePolicy(sizePolicy)
        self.le_input.setObjectName("le_input")
        self.gridLayout.addWidget(self.le_input, 0, 0, 1, 1)
        self.bt_confirm = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bt_confirm.sizePolicy().hasHeightForWidth())
        self.bt_confirm.setSizePolicy(sizePolicy)
        self.bt_confirm.setObjectName("bt_confirm")
        self.gridLayout.addWidget(self.bt_confirm, 0, 1, 1, 1)
        self.cb_quality = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_quality.sizePolicy().hasHeightForWidth())
        self.cb_quality.setSizePolicy(sizePolicy)
        self.cb_quality.setToolTip("")
        self.cb_quality.setObjectName("cb_quality")
        self.gridLayout.addWidget(self.cb_quality, 0, 2, 1, 1)
        self.tb_infos = QtWidgets.QTextBrowser(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_infos.sizePolicy().hasHeightForWidth())
        self.tb_infos.setSizePolicy(sizePolicy)
        self.tb_infos.setObjectName("tb_infos")
        self.gridLayout.addWidget(self.tb_infos, 1, 0, 1, 3)
        self.le_url = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_url.sizePolicy().hasHeightForWidth())
        self.le_url.setSizePolicy(sizePolicy)
        self.le_url.setObjectName("le_url")
        self.gridLayout.addWidget(self.le_url, 2, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def set_logic(self):
        self.bt_confirm.clicked.connect(self.confirm)
        self.cb_quality.activated.connect(self.show_url)
        
    def confirm(self):
        url=self.le_input.text()
        try:
            self.adds,self.title,self.infos=get_video(url)
            self.show_cover(self.infos['cover'])
            self.show_infos()
            self.update_cb()
            self.cb_quality.setCurrentIndex(0)
            self.show_url()
            
        except (Timeout,HTTPError,ConnectionError):
            exc=traceback.format_exc()
            QtWidgets.QMessageBox.warning(self,'Warning','Got exception:\n'+exc)
            self.tb_infos.setText(exc)

    def update_cb(self):
        qualities=list(self.adds.keys())
        self.cb_quality.addItems(qualities)
        
    def show_url(self):
        q=self.cb_quality.currentText()
        url=self.adds[q]
        self.le_url.setText(url)
        
    def show_cover(self,cover_url):
        print(cover_url)
        data=requests.get(cover_url,headers=self.headers,proxies=self.proxies).content
        qp = QtGui.QPixmap()
        qp.loadFromData(data)
        self.lb_cover.setPixmap(qp)
        
    def show_infos(self):
        text='Video title:{}\nDuration:{}\nAvailable qualities:{}\nCategories:{}'
        cats=','.join(self.infos['categories'])
        duration=self.infos['duration']
        qualities=','.join(list(self.adds.keys()))
        text=text.format(self.title,duration,qualities,cats)
        self.tb_infos.setText(text)
        
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PornHubDownloader", "PornHubDownloader"))
        self.lb_cover.setText(_translate("PornHubDownloader", "Video cover"))
        self.bt_confirm.setText(_translate("PornHubDownloader", "Confirm"))
        self.tb_infos.setText(_translate("PornHubDownloader", "Infos"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
