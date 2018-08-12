from PyQt5.Qt import *
import sys
import os


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
        self.setFixedSize(800, 600)

        rect = self.frameGeometry()
        rect.moveCenter(QApplication.desktop().availableGeometry().center())
        self.move(rect.topLeft())

        #ffmpeg文件选择
        ffmpegLabel = QLabel(self)
        ffmpegLabel.setAlignment(Qt.AlignCenter)
        ffmpegLabel.setFont(QFont("微软雅黑", 12))
        ffmpegLabel.setText("ffmpeg文件路径")
        ffmpegLabel.resize(ffmpegLabel.sizeHint())
        ffmpegLabel.move(self.width() / 2 - ffmpegLabel.width() / 2, 100)

        self.ffmpegLineEdit = QLineEdit(self)
        self.ffmpegLineEdit.setReadOnly(True)
        self.ffmpegLineEdit.resize(ffmpegLabel.size())
        self.ffmpegLineEdit.move(ffmpegLabel.x(),
                                 ffmpegLabel.y() + ffmpegLabel.height() + 10)

        ffmpegButton = QPushButton(self)
        ffmpegButton.setText("浏览")
        ffmpegButton.resize(ffmpegButton.sizeHint())
        ffmpegButton.move(
            self.ffmpegLineEdit.x() + self.ffmpegLineEdit.width() + 5,
            self.ffmpegLineEdit.y())
        ffmpegButton.clicked.connect(self.ffmpegButtonClicked)

        #.kux源文件选择
        srcDirLabel = QLabel(self)
        srcDirLabel.setAlignment(Qt.AlignCenter)
        srcDirLabel.setFont(QFont("微软雅黑", 12))
        srcDirLabel.setText(".kux源文件")
        srcDirLabel.resize(srcDirLabel.sizeHint())
        srcDirLabel.move(100, 300)

        self.srcDirLineEdit = QLineEdit(self)
        self.srcDirLineEdit.setReadOnly(True)
        self.srcDirLineEdit.resize(srcDirLabel.size())
        self.srcDirLineEdit.move(srcDirLabel.x(),
                                 srcDirLabel.y() + srcDirLabel.height() + 10)

        srcDirButton = QPushButton(self)
        srcDirButton.setText("浏览")
        srcDirButton.resize(srcDirButton.sizeHint())
        srcDirButton.move(
            self.srcDirLineEdit.x() + self.srcDirLineEdit.width() + 5,
            self.srcDirLineEdit.y())
        srcDirButton.clicked.connect(self.srcDirButtonClicked)

        #转换文件目标目录选择
        aimDirLabel = QLabel(self)
        aimDirLabel.setAlignment(Qt.AlignCenter)
        aimDirLabel.setFont(QFont("微软雅黑", 12))
        aimDirLabel.setText("转码目标文件目录")
        aimDirLabel.resize(aimDirLabel.sizeHint())
        aimDirLabel.move(srcDirButton.x() + srcDirButton.width() + 15,
                         srcDirLabel.y())

        self.aimDirLineEdit = QLineEdit(self)
        self.aimDirLineEdit.setReadOnly(True)
        self.aimDirLineEdit.resize(aimDirLabel.size())
        self.aimDirLineEdit.move(aimDirLabel.x(), self.srcDirLineEdit.y())

        aimDirButton = QPushButton(self)
        aimDirButton.setText("浏览")
        aimDirButton.resize(aimDirButton.sizeHint())
        aimDirButton.move(
            self.aimDirLineEdit.x() + self.aimDirLineEdit.width() +
            srcDirButton.x() - self.srcDirLineEdit.width() -
            self.srcDirLineEdit.x(), self.aimDirLineEdit.y())
        aimDirButton.clicked.connect(self.aimDirButtonClicked)

        #转码格式
        transcodeFormatlabel = QLabel(self)
        transcodeFormatlabel.setAlignment(Qt.AlignCenter)
        transcodeFormatlabel.setFont(QFont("微软雅黑", 12))
        transcodeFormatlabel.setText("转码格式")
        transcodeFormatlabel.resize(transcodeFormatlabel.sizeHint())
        transcodeFormatlabel.move(aimDirButton.x() + aimDirButton.width() + 15,
                                  aimDirLabel.y())

        self.transcodeFormatComboBox = QComboBox(self)
        self.transcodeFormatComboBox.addItem(".mp4")
        self.transcodeFormatComboBox.resize(
            self.transcodeFormatComboBox.sizeHint())
        self.transcodeFormatComboBox.move(
            transcodeFormatlabel.x(),
            transcodeFormatlabel.y() + transcodeFormatlabel.height() + 10)

        transcodeButton = QPushButton(self)
        transcodeButton.setFont(QFont("微软雅黑", 12))
        transcodeButton.setText("开始转码")
        transcodeButton.resize(transcodeButton.sizeHint())
        transcodeButton.move(self.width() / 2 - transcodeButton.width() / 2,
                             500)
        transcodeButton.clicked.connect(self.transcodeButtonClicked)

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
