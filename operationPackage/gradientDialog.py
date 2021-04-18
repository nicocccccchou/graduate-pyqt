from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GradientDialog(QDialog):
    def __init__(self, parent=None, flag=0):
        super(GradientDialog, self).__init__(parent)

        self.flag = flag

        self.setWindowTitle('GradientDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.gradientTypeLabel = QLabel(self)
        self.gradientTypeLabel.setText("算子类型")
        self.gradientTypeCB = QComboBox(self)
        self.gradientTypeCB.addItem("Sobel算子")
        self.gradientTypeCB.addItem("Scharr算子")
        self.gradientTypeCB.addItem("Laplacian算子")
        self.gradientTypeCB.currentIndexChanged.connect(self.selectionchange)

        self.ddepthLabel = QLabel(self)
        self.ddepthLabel.setText("目标图像的深度")
        self.ddepthCB = QComboBox(self)
        self.ddepthCB.addItem("CV_8U")
        self.ddepthCB.addItem("CV_16U")
        self.ddepthCB.addItem("CV_32F")
        self.ddepthCB.addItem("CV_64F")

        self.dxLabel = QLabel(self)
        self.dxLabel.setText("x方向上的导数阶数")
        self.dxLine = QLineEdit(self)

        self.dyLabel = QLabel(self)
        self.dyLabel.setText("y方向上的导数阶数")
        self.dyLine = QLineEdit(self)

        self.form.addRow(self.gradientTypeLabel, self.gradientTypeCB)
        self.form.addRow(self.ddepthLabel, self.ddepthCB)
        self.form.addRow(self.dxLabel, self.dxLine)
        self.form.addRow(self.dyLabel, self.dyLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.gradientTypeCB.currentText(), self.ddepthCB.currentText(), self.dxLine.text(), self.dyLine.text()

    def selectionchange(self, i):
        self.form.removeRow(3)
        self.form.removeRow(2)
        if i == 0 or i == 1:
            self.dxLabel = QLabel(self)
            self.dxLabel.setText("x方向上的导数阶数")
            self.dxLine = QLineEdit(self)

            self.dyLabel = QLabel(self)
            self.dyLabel.setText("x方向上的导数阶数")
            self.dyLine = QLineEdit(self)

            self.form.addRow(self.dxLabel, self.dxLine)
            self.form.addRow(self.dyLabel, self.dyLine)


