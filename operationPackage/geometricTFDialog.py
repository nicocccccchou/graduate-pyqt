from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class GeometricTFDialog(QDialog):
    def __init__(self, parent=None, flag=0):
        super(GeometricTFDialog, self).__init__(parent)

        self.flag = flag

        self.setWindowTitle('GeometricTFDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        if self.flag == 0:
            self.geometricTypeLabel = QLabel(self)
            self.geometricTypeLabel.setText("形态学操作类型")
            self.geometricTypeCB = QComboBox(self)
            self.geometricTypeCB.addItem("缩放")
            self.geometricTypeCB.addItem("翻转")
            self.geometricTypeCB.addItem("仿射")
            self.geometricTypeCB.addItem("透视")
            self.geometricTypeCB.currentIndexChanged.connect(self.selectionchange)

            self.dsizeLabel = QLabel(self)
            self.dsizeLabel.setText("输出图像大小")
            self.dsizeLine = QLineEdit(self)

            self.form.addRow(self.geometricTypeLabel, self.geometricTypeCB)
            self.form.addRow(self.dsizeLabel, self.dsizeLine)
        else:
            self.mapXLabel = QPushButton(self)
            self.mapXLabel.setText("导入映射的X值")
            self.mapXLine = QLineEdit(self)
            self.mapXLabel.clicked.connect(lambda: self.importImage(1))

            self.mapYLabel = QPushButton(self)
            self.mapYLabel.setText("导入映射的Y值")
            self.mapYLine = QLineEdit(self)
            self.mapYLabel.clicked.connect(lambda: self.importImage(2))

            self.interpolationTypeLabel = QLabel(self)
            self.interpolationTypeLabel.setText("插值方式")
            self.interpolationTypeCB = QComboBox(self)
            self.interpolationTypeCB.addItem("INTER_NEAREST")
            self.interpolationTypeCB.addItem("INTER_LINEAR")
            self.interpolationTypeCB.addItem("INTER_CUBIC")
            self.interpolationTypeCB.addItem("INTER_LANCZOS4")
            self.interpolationTypeCB.addItem("INTER_LINEAR_EXACT")
            self.interpolationTypeCB.addItem("WARP_FILL_OUTLIERS")
            self.interpolationTypeCB.addItem("WARP_INVERSE_MAP")

            self.form.addRow(self.mapXLabel, self.mapXLine)
            self.form.addRow(self.mapYLabel, self.mapYLine)
            self.form.addRow(self.interpolationTypeLabel, self.interpolationTypeCB)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        if self.flag == 0:
            if self.geometricTypeCB.currentText() == "缩放":
                return self.geometricTypeCB.currentText(), self.dsizeLine.text()
            elif self.geometricTypeCB.currentText() == "翻转":
                return self.geometricTypeCB.currentText(), self.flipCodeCB.currentText()
            elif self.geometricTypeCB.currentText() == "仿射":
                if self.isMCreateBox.isChecked():
                    return self.geometricTypeCB.currentText(), self.dsizeLine.text(), True, self.MCreateP1Line.text(), self.MCreateP2Line.text()
                else:
                    return self.geometricTypeCB.currentText(), self.dsizeLine.text(), False, self.MLine.text()
            else:
                if self.isMCreateBox.isChecked():
                    return self.geometricTypeCB.currentText(), self.dsizeLine.text(), False, self.MCreateP1Line.text(), self.MCreateP2Line.text()
                else:
                    return self.geometricTypeCB.currentText(), self.dsizeLine.text(), False, self.MLine.text()
        else:
            return self.mapXLine.text(), self.mapYLine.text(), self.interpolationTypeCB.currentText()

    def selectionchange(self, i):
        for index in range(int(self.form.count() / 2) - 1, 0, -1):
            self.form.removeRow(int(index))
        # if self.form.count() == 6:
        #     self.form.removeRow(2)
        # self.form.removeRow(1)

        if i == 0 or i == 2 or i == 3:
            self.dsizeLabel = QLabel(self)
            self.dsizeLabel.setText("输出图像大小")
            self.dsizeLine = QLineEdit(self)
            self.form.addRow(self.dsizeLabel, self.dsizeLine)
            if i == 2 or i == 3:
                self.isMCreateLabel = QLabel(self)
                self.isMCreateLabel.setText("生成变换矩阵")
                self.isMCreateBox = QCheckBox("")
                self.isMCreateBox.setChecked(False)
                self.isMCreateBox.stateChanged.connect(self.btnstate)

                self.MLabel = QPushButton(self)
                self.MLabel.setText("导入转换矩阵")
                self.MLine = QLineEdit(self)
                self.MLabel.clicked.connect(lambda: self.importImage(0))

                self.form.addRow(self.isMCreateLabel, self.isMCreateBox)
                self.form.addRow(self.MLabel, self.MLine)

        elif i == 1:
            self.flipCodeLabel = QLabel(self)
            self.flipCodeLabel.setText("形态学操作类型")
            self.flipCodeCB = QComboBox(self)
            self.flipCodeCB.addItem("绕x轴旋转")
            self.flipCodeCB.addItem("绕y轴旋转")
            self.flipCodeCB.addItem("绕原点旋转")
            self.form.addRow(self.flipCodeLabel, self.flipCodeCB)

    def btnstate(self):

        if self.isMCreateBox.isChecked() is True:
            index = self.form.count() / 2 - 1
            self.form.removeRow(index)
            self.MCreateP1Label = QLabel(self)
            self.MCreateP1Label.setText("生成变换矩阵")
            self.MCreateP1Line = QLineEdit(self)

            self.MCreateP2Label = QLabel(self)
            self.MCreateP2Label.setText("生成变换矩阵")
            self.MCreateP2Line = QLineEdit(self)

            self.form.addRow(self.MCreateP1Label, self.MCreateP1Line)
            self.form.addRow(self.MCreateP2Label, self.MCreateP2Line)

            if self.geometricTypeCB.currentIndex() == 2:
                self.MCreateP1Label.setText("输入图像的三个顶点的坐标")
                self.MCreateP1Line.setPlaceholderText("输入图像的三个点坐标，形如[[x1,y1],[x2,y2],[x3,y3]]")
                self.MCreateP2Label.setText("输出图像的三个顶点的坐标")
                self.MCreateP2Line.setPlaceholderText("输出图像的三个点坐标，形如[[x1,y1],[x2,y2],[x3,y3]]")
            elif self.geometricTypeCB.currentIndex() == 3:
                self.MCreateP1Label.setText("输入图像的四个顶点的坐标")
                self.MCreateP1Line.setPlaceholderText("输入图像的四个点坐标，形如[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]")
                self.MCreateP2Label.setText("输出图像的四个顶点的坐标")
                self.MCreateP2Line.setPlaceholderText("输出图像的四个点坐标，形如[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]")

        else:
            index = self.form.count() / 2 - 1
            self.form.removeRow(index)
            self.form.removeRow(index - 1)
            self.MLabel = QPushButton(self)
            self.MLabel.setText("导入转换矩阵")
            self.MLine = QLineEdit(self)
            self.MLabel.clicked.connect(lambda: self.importImage(0))
            self.form.addRow(self.MLabel, self.MLine)

    def importImage(self, flag):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传转换矩阵", "", "All Files(*)")
        if flag == 1:
            self.mapXLine.setText(imgName)
        elif flag == 2:
            self.mapYLine.setText(imgName)
        else:
            self.MLine.setText(imgName)
