from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ContourSelectDialog(QDialog):
    _signal = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, contourLen=None):
        super(ContourSelectDialog, self).__init__(parent)

        self.setWindowTitle('ContourSelectDialog')
        self.contourLen = contourLen
        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.contourSelectLabel = QLabel(self)
        self.contourSelectLabel.setText("轮廓选择")
        self.contourSelectCB = QComboBox(self)

        for i in range(self.contourLen):
            self.contourSelectCB.addItem(str(i))
        self.contourSelectCB.setMaxVisibleItems(10)
        self.contourSelectCB.currentIndexChanged.connect(self.selectionchange)
        self.contourSelectCB.setStyleSheet("QComboBox { combobox-popup: 0; }")
        self.form.addRow(self.contourSelectLabel,self.contourSelectCB)
        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.contourSelectCB.currentIndex()

    def selectionchange(self, i):
        self._signal.emit(i)
