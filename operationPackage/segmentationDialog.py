from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SegmentationDialog(QDialog):
    def __init__(self, parent=None):
        super(SegmentationDialog, self).__init__(parent)

        self.setWindowTitle('SegmentationDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.distanceTypeLabel = QLabel(self)
        self.distanceTypeLabel.setText("距离类型参数")
        self.distanceTypeCB = QComboBox(self)
        self.distanceTypeCB.addItem("DIST_L1")
        self.distanceTypeCB.addItem("DIST_L2")
        self.distanceTypeCB.addItem("DIST_C")
        self.distanceTypeCB.addItem("DIST_L12")
        self.distanceTypeCB.addItem("DIST_FAIR")
        self.distanceTypeCB.addItem("DIST_WELSCH")
        self.distanceTypeCB.addItem("DIST_HUBER")

        self.maskSizeLabel = QLabel(self)
        self.maskSizeLabel.setText("掩模的尺寸")
        self.maskSizeCB = QComboBox(self)
        self.maskSizeCB.addItem("DIST_MASK_3")
        self.maskSizeCB.addItem("DIST_MASK_5")
        self.maskSizeCB.addItem("DIST_MASK_PRECISE")

        self.thresholdRatioLabel = QLabel(self)
        self.thresholdRatioLabel.setText("阈值比率")
        self.thresholdRatioLine = QLineEdit(self)
        self.thresholdRatioLine.setPlaceholderText("阈值=阈值比率*dist_transform.max()")

        self.kernelLabel = QPushButton(self)
        self.kernelLabel.setText("导入核")
        self.kernelLabel.clicked.connect(self.importImage)
        self.kernelLine = QLineEdit(self)


        self.openIterationsLabel = QLabel(self)
        self.openIterationsLabel.setText("开运算迭代次数")
        self.openIterationsLine = QLineEdit(self)

        self.dilateIterationsLabel = QLabel(self)
        self.dilateIterationsLabel.setText("膨胀运算迭代次数")
        self.dilateIterationsLine = QLineEdit(self)

        self.form.addRow(self.distanceTypeLabel, self.distanceTypeCB)
        self.form.addRow(self.maskSizeLabel, self.maskSizeCB)
        self.form.addRow(self.thresholdRatioLabel, self.thresholdRatioLine)
        self.form.addRow(self.kernelLabel, self.kernelLine)
        self.form.addRow(self.openIterationsLabel, self.openIterationsLine)
        self.form.addRow(self.dilateIterationsLabel, self.dilateIterationsLine)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.distanceTypeCB.currentText(), self.maskSizeCB.currentText(), \
               self.thresholdRatioLine.text(), self.kernelLine.text(),\
               self.openIterationsLine.text(),self.dilateIterationsLine.text()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传模板图像", "", "All Files(*)")
        self.kernelLine.setText(imgName)
