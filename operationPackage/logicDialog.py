from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class LogicDialog(QDialog):
    def __init__(self, parent=None):
        super(LogicDialog, self).__init__(parent)
        self.setWindowTitle('bitOperationDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.logicTypeLabel = QLabel(self)
        self.logicTypeLabel.setText("按位操作类型")
        self.logicTypeCB = QComboBox(self)
        self.logicTypeCB.addItem("BITWISE_AND")
        self.logicTypeCB.addItem("BITWISE_OR")
        self.logicTypeCB.addItem("BITWISE_NOT")
        self.logicTypeCB.addItem("BITWISE_XOR")

        self.imageLabel = QPushButton(self)
        self.imageLabel.setText("导入图片")
        self.imageLabel.clicked.connect(self.importImage)
        self.imageLine = QLineEdit(self)

        self.form.addRow(self.logicTypeLabel, self.logicTypeCB)
        self.form.addRow(self.imageLabel, self.imageLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.logicTypeCB.currentText(), self.imageLine.text()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传图片", "", "*.jpg;;*.png;;All Files(*)")
        self.imageLine.setText(imgName)
