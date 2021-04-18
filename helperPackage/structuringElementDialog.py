import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class StructuringElementDialog(QDialog):
    def __init__(self, parent=None):
        super(StructuringElementDialog, self).__init__(parent)

        self.setWindowTitle('StructuringElementDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.shapeLabel = QLabel(self)
        self.shapeLabel.setText("形状类型")
        self.shapeTypeCB = QComboBox(self)
        self.shapeTypeCB.addItem("MORPH_RECT")
        self.shapeTypeCB.addItem("MORPH_CROSS")
        self.shapeTypeCB.addItem("MORPH_ELLIPSE")

        self.ksizeLabel = QLabel(self)
        self.ksizeLabel.setText("结构元素的大小")
        self.ksizeLine = QLineEdit(self)
        self.ksizeLine.setPlaceholderText("形如(5,5)")

        self.downloadLabel = QPushButton(self)
        self.downloadLabel.setText("选择下载地址")
        self.downloadLabel.clicked.connect(self.downloadMatrix)
        self.downloadLine = QLineEdit(self)

        self.form.addRow(self.shapeLabel, self.shapeTypeCB)
        self.form.addRow(self.ksizeLabel, self.ksizeLine)
        self.form.addRow(self.downloadLabel, self.downloadLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.shapeTypeCB.currentText(), self.ksizeLine.text()

    def downloadMatrix(self):
        downloadPath = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", os.getcwd())
        self.downloadLine.setText(downloadPath + "/structuringElement.txt")
