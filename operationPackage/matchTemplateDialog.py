from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MatchTemplateDialog(QDialog):
    def __init__(self, parent=None):
        super(MatchTemplateDialog, self).__init__(parent)

        self.setWindowTitle('MatchTemplateDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.templateLabel = QPushButton(self)
        self.templateLabel.setText("导入模板图像")
        self.templateLabel.clicked.connect(self.importImage)
        self.templateLine = QLineEdit(self)

        self.methodLabel = QLabel(self)
        self.methodLabel.setText("匹配方法")
        self.methodCB = QComboBox(self)
        self.methodCB.addItem("TM_SQDIFF")
        self.methodCB.addItem("TM_SQDIFF_NORMED")
        self.methodCB.addItem("TM_CCORR")
        self.methodCB.addItem("TM_CCORR_NORMED")
        self.methodCB.addItem("TM_CCOEFF")
        self.methodCB.addItem("TM_CCOEFF_NORMED")

        self.form.addRow(self.templateLabel, self.templateLine)
        self.form.addRow(self.methodLabel, self.methodCB)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.templateLine.text(), self.methodCB.currentText()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传模板图像", "", "*.jpg;;*.png;;All Files(*)")
        self.templateLine.setText(imgName)
