from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class AddDialog(QDialog):
    ##
    def __init__(self, parent=None, flag=None):
        """
        flag = 1表示单图片相加（与数字相加）
        flag = 2表示多图片相加
        flag = 3表示图片加权和
        :param parent:
        :param flag:
        """
        self.flag = flag

        super(AddDialog, self).__init__(parent)
        self.setWindowTitle('AddDialog')

        # 在布局中添加控件
        self.vLayout = QVBoxLayout(self)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.hLayout = QHBoxLayout(self)
        self.vLayout.addLayout(self.hLayout)
        if flag == 1:
            self.valueLabel = QLabel(self)
            self.valueLabel.setText("数值")
            self.valueLine = QLineEdit(self)
            self.hLayout.addWidget(self.valueLabel)
            self.hLayout.addWidget(self.valueLine)
        elif flag == 2:
            self.valueLabel = QPushButton(self)
            self.valueLabel.setText("导入图像")
            self.valueLabel.clicked.connect(self.importImage)
            self.valueLine = QLineEdit(self)
            self.hLayout.addWidget(self.valueLabel)
            self.hLayout.addWidget(self.valueLine)
        else:
            self.valueLabel = QPushButton(self)
            self.valueLabel.setText("导入图像")
            self.valueLabel.clicked.connect(self.importImage)
            self.valueLine = QLineEdit(self)
            self.hLayout.addWidget(self.valueLabel)
            self.hLayout.addWidget(self.valueLine)

            self.formLayout = QFormLayout(self)
            self.alphaLabel = QLabel(self)
            self.alphaLabel.setText("图像1权值")
            self.alphaText = QLineEdit(self)
            self.betaLabel = QLabel(self)
            self.betaLabel.setText("图像2权值")
            self.betaText = QLineEdit(self)
            self.gammaLabel = QLabel(self)
            self.gammaLabel.setText("亮度调节量")
            self.gammaText = QLineEdit(self)
            self.formLayout.addRow(self.alphaLabel, self.alphaText)
            self.formLayout.addRow(self.betaLabel, self.betaText)
            self.formLayout.addRow(self.gammaLabel, self.gammaText)
            self.vLayout.addLayout(self.formLayout)

        self.vLayout.addWidget(buttons)
        self.resize(400, 200)

    def getData(self):
        if self.flag == 1:
            return self.valueLine.text()
        elif self.flag == 2:
            return self.valueLine.text()
        else:
            return self.valueLine.text(), self.alphaText.text(), self.betaText.text(), self.gammaText.text()

    # def btnstate(self, b):
    #     if b.text() == "与数值相加":
    #         if b.isChecked() == True:
    #
    #             self.valueLabel = QLabel(self)
    #             self.valueLabel.setText("数值")
    #             self.valueLine = QLineEdit(self)
    #             self.hLayout1.addWidget(self.valueLabel)
    #             self.hLayout1.addWidget(self.valueLine)
    #
    #         else:
    #             for i in range(self.hLayout1.count()):
    #                 self.hLayout1.itemAt(i).widget().deleteLater()
    #
    #     if b.text() == "与图像相加":
    #         if b.isChecked() == True:
    #
    #             self.valueLabel = QPushButton(self)
    #             self.valueLabel.setText("导入图像")
    #             self.valueLabel.clicked.connect(self.importImage)
    #             self.valueLine = QLineEdit(self)
    #             self.hLayout1.addWidget(self.valueLabel)
    #             self.hLayout1.addWidget(self.valueLine)
    #
    #
    #         else:
    #             for i in range(self.hLayout1.count()):
    #                 self.hLayout1.itemAt(i).widget().deleteLater()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传图片", "", "*.jpg;;*.png;;All Files(*)")
        self.valueLine.setText(imgName)
