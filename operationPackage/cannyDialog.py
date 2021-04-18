from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CannyDialog(QDialog):
    def __init__(self, parent=None):
        super(CannyDialog, self).__init__(parent)

        self.setWindowTitle('CannyDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.minThreshValLabel = QLabel(self)
        self.minThreshValLabel.setText("低阈值minVal")
        self.minThreshValLine = QLineEdit(self)

        self.maxThreshValLabel = QLabel(self)
        self.maxThreshValLabel.setText("高阈值maxVal")
        self.maxThreshValLine = QLineEdit(self)

        self.apertureSizeLabel = QLabel(self)
        self.apertureSizeLabel.setText("Sobel算子的孔径大小")
        self.apertureSizeLine = QLineEdit(self)

        self.form.addRow(self.minThreshValLabel, self.minThreshValLine)
        self.form.addRow(self.maxThreshValLabel, self.maxThreshValLine)
        self.form.addRow(self.apertureSizeLabel, self.apertureSizeLine)



        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.minThreshValLine.text(),self.maxThreshValLine.text(),self.apertureSizeLine.text()
