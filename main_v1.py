import os.path
import re

from PyQt5.QtWidgets import QApplication,QWidget,QMessageBox
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "音乐下载器"))
        self.label.setText(_translate("Form", "请输入要下载的音乐"))
        self.pushButton.setText(_translate("Form", "搜索"))
        self.pushButton.clicked.connect(Form.btn_search)
        self.pushButton_2.setText(_translate("Form", "下一页"))
        self.pushButton_2.clicked.connect(Form.btn_next)
        self.pushButton_3.setText(_translate("Form", "清空"))
        self.pushButton_3.clicked.connect(Form.btn_clear)

        self.listWidget.itemDoubleClicked.connect(Form.download)
class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.page = 1
        self.dict = {}

    def btn_search(self,page):
        text = self.ui.lineEdit.text()

        from get_info import get_music
        track_info = get_music(text,page)
        # print(track_info)
        for track in track_info:
            title = track[0]
            singer = track[1]
            album = track[2]
            link = track[3]
            display_item = f'{title} - {singer} - {album}'
            self.dict[display_item] = link

            self.ui.listWidget.addItem(display_item)

    def btn_next(self):
        self.page += 1
        self.btn_search(self.page)

    def download(self,item):
        key = item.text()
        filename = re.sub('[/<>?]','',key)
        link = self.dict[key]

        msg = QMessageBox.information(self, '下载提示',f'是否下载{key}',QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                music_content = requests.get(link, headers=headers, timeout=60).content
                if not os.path.exists('下载'):
                    os.makedirs('下载')
                with open(f'下载/{filename}.mp3','wb') as f:
                    f.write(music_content)
                QMessageBox.warning(self, '下载提示','下载完成')
            except Exception as e:
                QMessageBox.warning(self, '下载提示', f'下载失败: {e}')

    def btn_clear(self):
        self.ui.listWidget.clear()
        self.ui.lineEdit.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())