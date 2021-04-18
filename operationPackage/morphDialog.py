from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class morphDialog(QDialog):
    def __init__(self, parent=None):
        super(morphDialog, self).__init__(parent)
        self.setWindowTitle('morphDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.morphTypeLabel = QLabel(self)
        self.morphTypeLabel.setText("形态学操作类型")
        self.morphCB = QComboBox(self)
        self.morphCB.addItem("MORPH_ERODE")
        self.morphCB.addItem("MORPH_DILATE")
        self.morphCB.addItem("MORPH_OPEN")
        self.morphCB.addItem("MORPH_CLOSE")
        self.morphCB.addItem("MORPH_GRADIENT")
        self.morphCB.addItem("MORPH_TOPHAT")
        self.morphCB.addItem("MORPH_BLACKHAT")
        self.morphCB.addItem("MORPH_HITMISS")

        self.iterationsLabel = QLabel(self)
        self.iterationsLabel.setText("迭代次数")
        self.iterationsLine = QLineEdit(self)

        self.isKernelCreateLabel = QLabel(self)
        self.isKernelCreateLabel.setText("生成结构元素矩阵")
        self.isKernelCreateBox = QCheckBox("")
        self.isKernelCreateBox.setChecked(True)
        self.isKernelCreateBox.stateChanged.connect(self.btnstate)

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

        self.form.addRow(self.morphTypeLabel, self.morphCB)
        # self.form.addRow(self.kernelLabel, self.kernelLine)
        self.form.addRow(self.iterationsLabel, self.iterationsLine)
        self.form.addRow(self.isKernelCreateLabel, self.isKernelCreateBox)
        self.form.addRow(self.shapeLabel, self.shapeTypeCB)
        self.form.addRow(self.ksizeLabel, self.ksizeLine)

        # self.hlayout.addWidget(self.maxValueLabel)
        # self.hlayout.addWidget(self.line)

        # layout.addLayout(self.hlayout)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        if self.isKernelCreateBox.isChecked() is True:
            return self.morphCB.currentText(), self.iterationsLine.text(), True, self.shapeTypeCB.currentText(), self.ksizeLine.text()
        else:
            return self.morphCB.currentText(), self.iterationsLine.text(), False, self.kernelLine.text()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传核", "", "All Files(*)")
        self.kernelLine.setText(imgName)

    def btnstate(self):
        if self.isKernelCreateBox.isChecked() is False:
            self.form.removeRow(4)
            self.form.removeRow(3)
            self.kernelLabel = QPushButton(self)
            self.kernelLabel.setText("导入核")
            self.kernelLabel.clicked.connect(self.importImage)
            self.kernelLine = QLineEdit(self)
            self.form.addRow(self.kernelLabel, self.kernelLine)
        else:
            self.form.removeRow(3)
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
            self.form.addRow(self.shapeLabel, self.shapeTypeCB)
            self.form.addRow(self.ksizeLabel, self.ksizeLine)
