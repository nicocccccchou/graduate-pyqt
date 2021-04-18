from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class ForegroundExtractionDialog(QDialog):
    def __init__(self, parent=None):
        super(ForegroundExtractionDialog, self).__init__(parent)

        self.setWindowTitle('ForegroundExtractionDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.maskLabel = QPushButton(self)
        self.maskLabel.setText("导入掩模图像")
        self.maskLabel.clicked.connect(self.importImage)
        self.maskLine = QLineEdit(self)

        self.rectLabel = QLabel(self)
        self.rectLabel.setText("前景对象的区域")
        self.rectLine = QLineEdit(self)
        self.rectLine.setPlaceholderText("请输入一个一维数组，类似于(50,50,400,400)")

        self.iterCountLabel = QLabel(self)
        self.iterCountLabel.setText("迭代次数")
        self.iterCountLine = QLineEdit(self)

        self.form.addRow(self.maskLabel, self.maskLine)
        self.form.addRow(self.rectLabel, self.rectLine)
        self.form.addRow(self.iterCountLabel, self.iterCountLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.maskLine.text(), self.rectLine.text(), self.iterCountLine.text()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传模板图像", "", "*.jpg;;*.png;;All Files(*)")
        self.maskLine.setText(imgName)

