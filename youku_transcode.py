from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import os
from pathlib import Path


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ffmpegDir = ""
        self.srcDir = ""
        self.aimDir = ""
        self.transcodeFormat = ""

        self.initUI()

    def initUI(self):
        self.setWindowTitle("优酷转码GUI工具")

        rect = self.frameGeometry()
        rect.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(rect.topLeft())

        #ffmpeg文件选择
        ffmpegLabel = QLabel(self)
        ffmpegLabel.setAlignment(Qt.AlignCenter)
        ffmpegLabel.setFont(QFont("微软雅黑", 12))
        ffmpegLabel.setText("ffmpeg文件路径")

        self.ffmpegLineEdit = QLineEdit(self)
        self.ffmpegLineEdit.setReadOnly(True)
        # 默认ffmpeg
        p = Path(__file__).resolve().parent / 'nplayer' / 'ffmpeg.exe'
        self.ffmpegLineEdit.setText(str(p))

        ffmpegButton = QPushButton(self)
        ffmpegButton.setText("浏览")
        ffmpegButton.clicked.connect(self.ffmpegButtonClicked)

        #.kux源文件选择
        srcDirLabel = QLabel(self)
        srcDirLabel.setAlignment(Qt.AlignCenter)
        srcDirLabel.setFont(QFont("微软雅黑", 12))
        srcDirLabel.setText(".kux源文件")

        self.srcDirLineEdit = QLineEdit(self)
        self.srcDirLineEdit.setReadOnly(True)

        srcDirButton = QPushButton(self)
        srcDirButton.setText("浏览")
        srcDirButton.clicked.connect(self.srcDirButtonClicked)

        #转换文件目标目录选择
        aimDirLabel = QLabel(self)
        aimDirLabel.setAlignment(Qt.AlignCenter)
        aimDirLabel.setFont(QFont("微软雅黑", 12))
        aimDirLabel.setText("转码目标文件目录")

        self.aimDirLineEdit = QLineEdit(self)
        self.aimDirLineEdit.setReadOnly(True)

        aimDirButton = QPushButton(self)
        aimDirButton.setText("浏览")
        aimDirButton.clicked.connect(self.aimDirButtonClicked)

        #转码格式
        transcodeFormatlabel = QLabel(self)
        transcodeFormatlabel.setAlignment(Qt.AlignCenter)
        transcodeFormatlabel.setFont(QFont("微软雅黑", 12))
        transcodeFormatlabel.setText("转码格式")

        self.transcodeFormatComboBox = QComboBox(self)
        self.transcodeFormatComboBox.addItem(".mp4")

        transcodeButton = QPushButton(self)
        transcodeButton.setFont(QFont("微软雅黑", 12))
        transcodeButton.setText("开始转码")
        transcodeButton.clicked.connect(self.transcodeButtonClicked)

        # 布局
        layout = QGridLayout(self)
        layout.addWidget(ffmpegLabel, 0, 0, 1, 1)
        layout.addWidget(self.ffmpegLineEdit, 0, 1, 1, 1)
        layout.addWidget(ffmpegButton, 0, 2, 1, 1)
        layout.addWidget(srcDirLabel, 1, 0, 1, 1)
        layout.addWidget(self.srcDirLineEdit, 1, 1, 1, 1)
        layout.addWidget(srcDirButton, 1, 2, 1, 1)
        layout.addWidget(aimDirLabel, 2, 0, 1, 1)
        layout.addWidget(self.aimDirLineEdit, 2, 1, 1, 1)
        layout.addWidget(aimDirButton, 2, 2, 1, 1)
        layout.addWidget(transcodeFormatlabel, 3, 0, 1, 1)
        layout.addWidget(self.transcodeFormatComboBox, 3, 1, 1, 1)
        layout.addWidget(transcodeButton, 3, 2, 1, 1)

    def ffmpegButtonClicked(self):
        self.ffmpegDir = QFileDialog.getOpenFileName(self, "ffmpeg路径选择")[0]
        if self.ffmpegDir != "":
            self.ffmpegLineEdit.setText(self.ffmpegDir)

    def srcDirButtonClicked(self):
        self.srcDir = QFileDialog.getOpenFileNames(self, ".kux源文件选择")[0]
        if len(self.srcDir) != 0:
            self.srcDirLineEdit.setText(", ".join(self.srcDir))

    def aimDirButtonClicked(self):
        self.aimDir = QFileDialog.getExistingDirectory(self, "生成文件目标目录选择")
        if self.aimDir != "":
            self.aimDirLineEdit.setText(self.aimDir)

    def transcodeButtonClicked(self):
        if self.ffmpegDir == "":
            QMessageBox.warning(self, "警告", "ffmpeg文件路径不可为空！")
        elif self.srcDir == "":
            QMessageBox.warning(self, "警告", ".kux源文件路径不可为空！")
        elif self.aimDir == "":
            QMessageBox.warning(self, "警告", "生成文件目标目录不可为空！")
        else:
            for i in self.srcDir:
                if i.split('.')[1] == "kux":
                    os.popen(  #不知道为什么用os.system就会各种命令出错，就好像同时在使用cmd和power shell，搞不懂
                        "\"" + self.ffmpegDir + "\"" + " -y -i " + "\"" + i +
                        "\"" + " -c:v copy -c:a copy -threads 2 " + "\"" +
                        self.aimDir + "/" + i.split('/')[-1].split('.')[0] +
                        self.transcodeFormatComboBox.currentText() + "\"")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
