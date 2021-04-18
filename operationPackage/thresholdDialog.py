from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ThresholdDialog(QDialog):
    def __init__(self, parent=None, flag=0):
        super(ThresholdDialog, self).__init__(parent)
        self.flag = flag

        self.setWindowTitle('ThresholdDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        if self.flag == 0:
            self.thresholdTypeLabel = QLabel(self)
            self.thresholdTypeLabel.setText("阈值分割类型")
            self.cb = QComboBox(self)
            self.cb.addItem("THRESH_BINARY")
            self.cb.addItem("THRESH_BINARY_INV")
            self.cb.addItem("THRESH_TRUNC")
            self.cb.addItem("THRESH_TOZERO")
            self.cb.addItem("THRESH_TOZERO_INV")

            self.globalThresholdLabel = QLabel(self)
            self.globalThresholdLabel.setText("全局阈值类型")
            self.cb1 = QComboBox(self)
            self.cb1.addItem("    ")
            self.cb1.addItem("THRESH_OTSU")
            self.cb1.addItem("THRESH_TRIANGLE")

            self.threshLabel = QLabel(self)
            self.threshLabel.setText("阈值")
            self.threshLine = QLineEdit(self)

            self.form.addRow(self.thresholdTypeLabel, self.cb)
            self.form.addRow(self.globalThresholdLabel, self.cb1)
            self.form.addRow(self.threshLabel, self.threshLine)

        else:
            self.thresholdTypeLabel = QLabel(self)
            self.thresholdTypeLabel.setText("阈值分割类型")
            self.cb = QComboBox(self)
            self.cb.addItem("THRESH_BINARY")
            self.cb.addItem("THRESH_BINARY_INV")

            self.adaptiveMethodLabel = QLabel(self)
            self.adaptiveMethodLabel.setText("自适应方法")
            self.adaptiveMethodCB = QComboBox(self)
            self.adaptiveMethodCB.addItem("ADAPTIVE_THRESH_GAUSSIAN_C")
            self.adaptiveMethodCB.addItem("ADAPTIVE_THRESH_MEAN_C")

            self.blockSizeLabel = QLabel(self)
            self.blockSizeLabel.setText("块大小")
            self.blockSizeLine = QLineEdit(self)

            self.CLabel = QLabel(self)
            self.CLabel.setText("常量C")
            self.CLine = QLineEdit(self)

            self.form.addRow(self.thresholdTypeLabel, self.cb)
            self.form.addRow(self.adaptiveMethodLabel, self.adaptiveMethodCB)
            self.form.addRow(self.blockSizeLabel, self.blockSizeLine)
            self.form.addRow(self.CLabel, self.CLine)

        self.maxValueLabel = QLabel(self)
        self.maxValueLabel.setText("最大值")
        self.maxValueLine = QLineEdit(self)

        self.form.addRow(self.maxValueLabel, self.maxValueLine)

        # self.hlayout.addWidget(self.maxValueLabel)
        # self.hlayout.addWidget(self.line)

        # layout.addLayout(self.hlayout)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getForm(self):
        if self.flag == 0:
            return self.cb.currentText(), self.cb1.currentText(), self.threshLine.text(), self.maxValueLine.text()
        else:
            return self.cb.currentIndex(), self.adaptiveMethodCB.currentIndex(), self.blockSizeLine.text(), self.CLine.text(), self.maxValueLine.text()
