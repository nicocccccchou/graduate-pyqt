from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class HoughTFDialog(QDialog):
    def __init__(self, parent=None, flag=0):
        super(HoughTFDialog, self).__init__(parent)

        self.flag = flag

        self.setWindowTitle('HoughTFDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        if flag == 0:

            self.rhoLabel = QLabel(self)
            self.rhoLabel.setText("极坐标的极径r的精度")
            self.rhoLine = QLineEdit(self)

            self.thetaLabel = QLabel(self)
            self.thetaLabel.setText("极坐标的极角𝜃的精度")
            self.thetaLine = QLineEdit(self)

            self.thresholdLabel = QLabel(self)
            self.thresholdLabel.setText("阈值")
            self.thresholdLine = QLineEdit(self)

            self.optimizeLabel = QLabel(self)
            self.optimizeLabel.setText("是否需要优化")
            self.optimizeButton = QCheckBox("")
            self.optimizeButton.setChecked(True)
            self.optimizeButton.stateChanged.connect(self.btnstate)

            self.minLineLengthLabel = QLabel(self)
            self.minLineLengthLabel.setText("直线的最小长度")
            self.minLineLengthLine = QLineEdit(self)
            self.minLineLengthLine.setText("0")

            self.maxLineGapLabel = QLabel(self)
            self.maxLineGapLabel.setText("共线线段之间的最小间隔")
            self.maxLineGapLine = QLineEdit(self)
            self.maxLineGapLine.setText("0")

            self.form.addRow(self.rhoLabel, self.rhoLine)
            self.form.addRow(self.thetaLabel, self.thetaLine)
            self.form.addRow(self.thresholdLabel, self.thresholdLine)
            self.form.addRow(self.optimizeLabel, self.optimizeButton)
            self.form.addRow(self.minLineLengthLabel, self.minLineLengthLine)
            self.form.addRow(self.maxLineGapLabel, self.maxLineGapLine)

        else:

            self.dpLabel = QLabel(self)
            self.dpLabel.setText("累计器分辨率")
            self.dpLine = QLineEdit(self)

            self.minDistLabel = QLabel(self)
            self.minDistLabel.setText("圆心间的最小间距")
            self.minDistLine = QLineEdit(self)

            self.param1Label = QLabel(self)
            self.param1Label.setText("对应Canny边缘检测器的高阈值")
            self.param1Line = QLineEdit(self)

            self.param2Label = QLabel(self)
            self.param2Label.setText("圆心位置必须收到的投票数")
            self.param2Line = QLineEdit(self)

            self.minRadiusLabel = QLabel(self)
            self.minRadiusLabel.setText("圆半径的最小值")
            self.minRadiusLine = QLineEdit(self)

            self.maxRadiusLabel = QLabel(self)
            self.maxRadiusLabel.setText("圆半径的最大值")
            self.maxRadiusLine = QLineEdit(self)

            self.form.addRow(self.dpLabel, self.dpLine)
            self.form.addRow(self.minDistLabel, self.minDistLine)
            self.form.addRow(self.param1Label, self.param1Line)
            self.form.addRow(self.param2Label, self.param2Line)
            self.form.addRow(self.minRadiusLabel, self.minRadiusLine)
            self.form.addRow(self.maxRadiusLabel, self.maxRadiusLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        if self.flag == 0:
            return self.rhoLine.text(), self.thetaLine.text(), self.thresholdLine.text(), \
                   self.optimizeButton.isChecked(),self.minLineLengthLine.text(), self.maxLineGapLine.text()
        else:
            return self.dpLine.text(), self.minDistLine.text(), self.param1Line.text(), \
                   self.param2Line.text(), self.minRadiusLine.text(), self.maxRadiusLine.text()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传模板图像", "", "*.jpg;;*.png;;All Files(*)")
        self.templateLine.setText(imgName)

    def btnstate(self):
        if self.optimizeButton.isChecked() is True:
            self.minLineLengthLabel = QLabel(self)
            self.minLineLengthLabel.setText("直线的最小长度")
            self.minLineLengthLine = QLineEdit(self)
            self.minLineLengthLine.setText("0")

            self.maxLineGapLabel = QLabel(self)
            self.maxLineGapLabel.setText("共线线段之间的最小间隔")
            self.maxLineGapLine = QLineEdit(self)
            self.maxLineGapLine.setText("0")

            self.form.addRow(self.minLineLengthLabel, self.minLineLengthLine)
            self.form.addRow(self.maxLineGapLabel, self.maxLineGapLine)
        else:
            self.form.removeRow(5)
            self.form.removeRow(4)
