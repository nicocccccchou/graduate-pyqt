from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class samplingDialog(QDialog):
    def __init__(self, parent=None, flag=None):
        super(samplingDialog, self).__init__(parent)

        self.setWindowTitle('samplingDialog')
        self.flag = flag
        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.sampleTypeLabel = QLabel(self)
        self.sampleTypeLabel.setText("取样类型")
        self.sampleTypeCB = QComboBox(self)
        self.sampleTypeCB.addItem("向下取样")
        self.sampleTypeCB.addItem("向上取样")
        self.sampleTypeCB.currentIndexChanged.connect(self.selectionchange)

        self.iterationLabel = QLabel(self)
        self.iterationLabel.setText("迭代次数")
        self.iterationLine = QLineEdit(self)

        self.isLaplacianLabel = QLabel(self)
        self.isLaplacianLabel.setText("是否需要保存拉普拉斯金字塔")
        self.isLaplacianButton = QCheckBox("")
        self.isLaplacianButton.setChecked(False)
        # self.isLaplacianButton.stateChanged.connect(self.btnstate)

        self.form.addRow(self.sampleTypeLabel, self.sampleTypeCB)
        self.form.addRow(self.iterationLabel, self.iterationLine)
        self.form.addRow(self.isLaplacianLabel, self.isLaplacianButton)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        if self.sampleTypeCB.currentText() == "向下取样":
            return self.sampleTypeCB.currentText(), self.iterationLine.text(), self.isLaplacianButton.isChecked()
        else:
            if self.flag is True:
                return self.sampleTypeCB.currentText(), self.iterationLine.text(), self.isLaplacianButton.isChecked()
            else:
                return self.sampleTypeCB.currentText(), self.iterationLine.text()

    def selectionchange(self, i):
        if self.form.count() == 8:
            self.form.removeRow(3)
        if i == 0:
            if self.form.count() == 4:
                self.isLaplacianLabel = QLabel(self)
                self.isLaplacianLabel.setText("是否需要保存拉普拉斯金字塔")
                self.isLaplacianButton = QCheckBox("")
                self.isLaplacianButton.setChecked(False)
                self.form.addRow(self.isLaplacianLabel, self.isLaplacianButton)
            else:
                self.isLaplacianLabel.setText("是否需要保存拉普拉斯金字塔")
        else:
            if self.flag is True:
                self.isLaplacianLabel.setText("是否需要拉普拉斯金字塔进行向上取样")
            else:
                self.form.removeRow(2)
