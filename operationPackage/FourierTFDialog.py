from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FourierTFDialog(QDialog):
    def __init__(self, parent=None):
        super(FourierTFDialog, self).__init__(parent)

        self.setWindowTitle('FourierTFDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.maskLabel = QPushButton(self)
        self.maskLabel.setText("导入滤波掩模图像")
        self.maskLabel.clicked.connect(self.importImage)
        self.maskLine = QLineEdit(self)

        self.form.addRow(self.maskLabel, self.maskLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.maskLine.text()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传模板图像", "", "*.jpg;;*.png;;All Files(*)")
        self.maskLine.setText(imgName)
