import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AffineTransformMatrixDialog(QDialog):
    def __init__(self, parent=None):
        super(AffineTransformMatrixDialog, self).__init__(parent)

        self.setWindowTitle('AffineTransformMatrixDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.srcLabel = QLabel(self)
        self.srcLabel.setText("输入图像的三个顶点的坐标")
        self.srcLine = QLineEdit(self)
        self.srcLine.setPlaceholderText("输入图像的三个点坐标，形如[[x1,y1],[x2,y2],[x3,y3]]")

        self.dstLabel = QLabel(self)
        self.dstLabel.setText("输出图像的三个顶点的坐标")
        self.dstLine = QLineEdit(self)
        self.dstLine.setPlaceholderText("输出图像的三个点坐标，形如[[x1,y1],[x2,y2],[x3,y3]]")

        self.downloadLabel = QPushButton(self)
        self.downloadLabel.setText("选择下载地址")
        self.downloadLabel.clicked.connect(self.downloadMatrix)
        self.downloadLine = QLineEdit(self)

        self.form.addRow(self.srcLabel, self.srcLine)
        self.form.addRow(self.dstLabel, self.dstLine)
        self.form.addRow(self.downloadLabel, self.downloadLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.srcLine.text(), self.dstLine.text(), self.downloadLine.text()

    def downloadMatrix(self):
        downloadPath = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", os.getcwd())
        self.downloadLine.setText(downloadPath + "/affineTransformMatrix.txt")
