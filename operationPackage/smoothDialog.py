import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SmoothDialog(QDialog):
    def __init__(self, parent=None, flag=0):
        super(SmoothDialog, self).__init__(parent)

        self.flag = flag

        self.setWindowTitle('smoothDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        if flag == 0:

            self.smoothTypeLabel = QLabel(self)
            self.smoothTypeLabel.setText("滤波类型")
            self.smoothTypeCB = QComboBox(self)
            self.smoothTypeCB.addItem("均值滤波")
            self.smoothTypeCB.addItem("方框滤波")
            self.smoothTypeCB.addItem("高斯滤波")
            self.smoothTypeCB.addItem("中值滤波")
            self.smoothTypeCB.addItem("双边滤波")
            self.smoothTypeCB.currentIndexChanged.connect(self.selectionchange)

            self.ksizeLabel = QLabel(self)
            self.ksizeLabel.setText("滤波核大小")
            self.ksizeLabel.setFocus()
            self.ksizeLine = QLineEdit(self)
            self.ksizeLine.setProperty("name", "smoothKsizeLine")
            self.ksizeLine.setPlaceholderText("滤波核形如(5,5)")
            self.form.addRow(self.smoothTypeLabel, self.smoothTypeCB)
            self.form.addRow(self.ksizeLabel, self.ksizeLine)
        else:
            # self.ksizeLabel = QLabel(self)
            # self.ksizeLabel.setText("修正值")
            # self.ksizeLine = QLineEdit(self)

            self.kernelLabel = QPushButton(self)
            self.kernelLabel.setText("导入卷积核")
            self.kernelLabel.clicked.connect(self.importImage)
            self.kernelLine = QLineEdit(self)

            # self.form.addRow(self.ksizeLabel, self.ksizeLine)
            self.form.addRow(self.kernelLabel, self.kernelLine)
        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        if self.flag == 0:
            if self.smoothTypeCB.currentText() == "均值滤波":
                return self.smoothTypeCB.currentText(), self.ksizeLine.text()
            elif self.smoothTypeCB.currentText() == "方框滤波":
                return self.smoothTypeCB.currentText(), self.ksizeLine.text(), self.ddepthLine.text()
            elif self.smoothTypeCB.currentText() == "高斯滤波":
                return self.smoothTypeCB.currentText(), self.ksizeLine.text(), self.sigmaXLine.text(), self.sigmaYLine.text()
            elif self.smoothTypeCB.currentText() == "中值滤波":
                return self.smoothTypeCB.currentText(), self.ksizeLine.text()
            else:
                return self.smoothTypeCB.currentText(), self.ksizeLine.text(), self.sigmaXLine.text(), self.sigmaYLine.text()
        else:
            return self.kernelLine.text()

    def selectionchange(self, i):
        for row in range(int(self.form.count() / 2) - 1, 1, -1):
            self.form.removeRow(row)
        self.ksizeLabel.setText("滤波核大小")
        if i == 1:
            self.ddepthLabel = QLabel(self)
            self.ddepthLabel.setText("处理结果图像的图像深度")
            self.ddepthLine = QLineEdit(self)
            self.form.addRow(self.ddepthLabel, self.ddepthLine)
        elif i == 2:
            self.sigmaXLabel = QLabel(self)
            self.sigmaXLabel.setText("卷积核在水平方向上的标准差")
            self.sigmaXLine = QLineEdit(self)
            self.sigmaXLine.setText("0")

            self.sigmaYLabel = QLabel(self)
            self.sigmaYLabel.setText("卷积核在垂直方向上的标准差")
            self.sigmaYLine = QLineEdit(self)
            self.sigmaYLine.setText("0")

            self.form.addRow(self.sigmaXLabel, self.sigmaXLine)
            self.form.addRow(self.sigmaYLabel, self.sigmaYLine)
        elif i == 3:
            self.ksizeLine.setPlaceholderText("滤波核大小,形如5")
        elif i == 4:
            self.ksizeLabel.setText("以当前像素点为中心点的直径")
            self.ksizeLine.setPlaceholderText("空间距离参数")
            self.sigmaXLabel = QLabel(self)
            self.sigmaXLabel.setText("颜色差值范围")
            self.sigmaXLine = QLineEdit(self)

            self.sigmaYLabel = QLabel(self)
            self.sigmaYLabel.setText("坐标空间中sigma值")
            self.sigmaYLine = QLineEdit(self)

            self.form.addRow(self.sigmaXLabel, self.sigmaXLine)
            self.form.addRow(self.sigmaYLabel, self.sigmaYLine)

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传核", os.getcwd(), "All Files(*)")
        self.kernelLine.setText(imgName)
