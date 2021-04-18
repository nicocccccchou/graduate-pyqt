import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class RotationMatrix2DDialog(QDialog):
    def __init__(self, parent=None):
        super(RotationMatrix2DDialog, self).__init__(parent)

        self.setWindowTitle('RotationMatrix2DDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.centerValLabel = QLabel(self)
        self.centerValLabel.setText("旋转的中心点")
        self.centerValLine = QLineEdit(self)
        self.centerValLine.setPlaceholderText("放射旋转变换中心点，形如(x,y)")

        self.angleValLabel = QLabel(self)
        self.angleValLabel.setText("旋转角度")
        self.angleValLine = QLineEdit(self)
        self.angleValLine.setPlaceholderText("正数表示逆时针旋转，负数表示顺时针旋转")

        self.scaleLabel = QLabel(self)
        self.scaleLabel.setText("变换尺度")
        self.scaleLine = QLineEdit(self)

        self.downloadLabel = QPushButton(self)
        self.downloadLabel.setText("选择下载地址")
        self.downloadLabel.clicked.connect(self.downloadMatrix)
        self.downloadLine = QLineEdit(self)

        self.form.addRow(self.centerValLabel, self.centerValLine)
        self.form.addRow(self.angleValLabel, self.angleValLine)
        self.form.addRow(self.scaleLabel, self.scaleLine)
        self.form.addRow(self.downloadLabel, self.downloadLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.centerValLine.text(), self.angleValLine.text(), self.scaleLine.text(), self.downloadLine.text()

    def downloadMatrix(self):
        downloadPath = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", os.getcwd())
        self.downloadLine.setText(downloadPath + "/rotationMatrix.txt")
