from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ContoursDialog(QDialog):
    def __init__(self, parent=None):
        super(ContoursDialog, self).__init__(parent)

        self.setWindowTitle('ContoursDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.modeLabel = QLabel(self)
        self.modeLabel.setText("轮廓检索模式")
        self.modeCB = QComboBox(self)
        self.modeCB.addItem("RETR_CCOMP")
        self.modeCB.addItem("RETR_EXTERNAL")
        self.modeCB.addItem("RETR_LIST")
        self.modeCB.addItem("RETR_TREE")
        self.modeCB.addItem("RETR_FLOODFILL")

        self.methodLabel = QLabel(self)
        self.methodLabel.setText("轮廓检索模式")
        self.methodCB = QComboBox(self)
        self.methodCB.addItem("CHAIN_APPROX_NONE")
        self.methodCB.addItem("CHAIN_APPROX_SIMPLE")
        self.methodCB.addItem("CHAIN_APPROX_TC89_KCOS")
        self.methodCB.addItem("CHAIN_APPROX_TC89_L1")

        self.isThresholdLabel = QLabel(self)
        self.isThresholdLabel.setText("是否需要阈值处理")
        self.isThresholdBox = QCheckBox("")
        self.isThresholdBox.setChecked(True)
        self.isThresholdBox.stateChanged.connect(self.btnstate)

        self.thresholdTypeLabel = QLabel(self)
        self.thresholdTypeLabel.setText("阈值分割类型")
        self.thresholdTypeCB = QComboBox(self)
        self.thresholdTypeCB.addItem("THRESH_BINARY")
        self.thresholdTypeCB.addItem("THRESH_BINARY_INV")
        self.thresholdTypeCB.addItem("THRESH_TRUNC")
        self.thresholdTypeCB.addItem("THRESH_TOZERO")
        self.thresholdTypeCB.addItem("THRESH_TOZERO_INV")

        self.globalThresholdLabel = QLabel(self)
        self.globalThresholdLabel.setText("全局阈值类型")
        self.globalThresholdCB = QComboBox(self)
        self.globalThresholdCB.addItem("    ")
        self.globalThresholdCB.addItem("THRESH_OTSU")
        self.globalThresholdCB.addItem("THRESH_TRIANGLE")

        self.threshLabel = QLabel(self)
        self.threshLabel.setText("阈值")
        self.threshLine = QLineEdit(self)

        self.maxValueLabel = QLabel(self)
        self.maxValueLabel.setText("最大值")
        self.maxValueLine = QLineEdit(self)

        self.form.addRow(self.modeLabel, self.modeCB)
        self.form.addRow(self.methodLabel, self.methodCB)
        self.form.addRow(self.isThresholdLabel, self.isThresholdBox)
        self.form.addRow(self.thresholdTypeLabel, self.thresholdTypeCB)
        self.form.addRow(self.globalThresholdLabel, self.globalThresholdCB)
        self.form.addRow(self.threshLabel, self.threshLine)
        self.form.addRow(self.maxValueLabel, self.maxValueLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        if self.isThresholdBox.isChecked() is True:
            return self.isThresholdBox.isChecked(), self.modeCB.currentText(), \
                   self.methodCB.currentText(), self.thresholdTypeCB.currentText(), \
                   self.globalThresholdCB.currentText(), self.threshLine.text(), \
                   self.maxValueLine.text()
        else:
            return self.isThresholdBox.isChecked(), self.modeCB.currentText(), \
                   self.methodCB.currentText()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传核", "", "All Files(*)")
        self.kernelLine.setText(imgName)

    def btnstate(self):
        if self.isThresholdBox.isChecked() is True:
            self.thresholdTypeLabel = QLabel(self)
            self.thresholdTypeLabel.setText("阈值分割类型")
            self.thresholdTypeCB = QComboBox(self)
            self.thresholdTypeCB.addItem("THRESH_BINARY")
            self.thresholdTypeCB.addItem("THRESH_BINARY_INV")
            self.thresholdTypeCB.addItem("THRESH_TRUNC")
            self.thresholdTypeCB.addItem("THRESH_TOZERO")
            self.thresholdTypeCB.addItem("THRESH_TOZERO_INV")

            self.globalThresholdLabel = QLabel(self)
            self.globalThresholdLabel.setText("全局阈值类型")
            self.globalThresholdCB = QComboBox(self)
            self.globalThresholdCB.addItem("    ")
            self.globalThresholdCB.addItem("THRESH_OTSU")
            self.globalThresholdCB.addItem("THRESH_TRIANGLE")

            self.threshLabel = QLabel(self)
            self.threshLabel.setText("阈值")
            self.threshLine = QLineEdit(self)

            self.maxValueLabel = QLabel(self)
            self.maxValueLabel.setText("最大值")
            self.maxValueLine = QLineEdit(self)

            self.form.addRow(self.thresholdTypeLabel, self.thresholdTypeCB)
            self.form.addRow(self.globalThresholdLabel, self.globalThresholdCB)
            self.form.addRow(self.threshLabel, self.threshLine)
            self.form.addRow(self.maxValueLabel, self.maxValueLine)
        else:
            self.form.removeRow(6)
            self.form.removeRow(5)
            self.form.removeRow(4)
            self.form.removeRow(3)

