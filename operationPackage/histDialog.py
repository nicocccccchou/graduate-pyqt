from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class HistDialog(QDialog):
    def __init__(self, parent=None, flag=0):
        super(HistDialog, self).__init__(parent)

        self.flag = flag

        self.setWindowTitle('HistDialog')

        # 在布局中添加控件
        layout = QVBoxLayout(self)
        self.form = QFormLayout(self)

        self.channelsLabel = QLabel(self)
        self.channelsLabel.setText("指定通道编号")
        self.channelsLine = QLineEdit(self)

        self.maskLabel = QPushButton(self)
        self.maskLabel.setText("导入掩模图像")
        self.maskLabel.clicked.connect(self.importImage)
        self.maskLine = QLineEdit(self)

        self.histSizeLabel = QLabel(self)
        self.histSizeLabel.setText("参数子集数目BINS值")
        self.histSizeLine = QLineEdit(self)

        self.rangesLabel = QLabel(self)
        self.rangesLabel.setText("像素值范围")
        self.rangesHLayout = QHBoxLayout(self)
        self.rangeStartLine = QLineEdit(self)
        self.lineLabel = QLabel(self)
        self.lineLabel.setText("——")
        self.rangeEndLine = QLineEdit(self)
        self.rangesHLayout.addWidget(self.rangeStartLine)
        self.rangesHLayout.addWidget(self.lineLabel)
        self.rangesHLayout.addWidget(self.rangeEndLine)

        self.accumulateLabel = QLabel(self)
        self.accumulateLabel.setText("是否累计计算")
        self.accumulateBox = QCheckBox("")
        self.accumulateBox.setChecked(False)

        self.equalLabel = QLabel(self)
        self.equalLabel.setText("是否需要均衡化")
        self.equalBox = QCheckBox("")
        self.equalBox.setChecked(True)

        self.form.addRow(self.channelsLabel, self.channelsLine)
        self.form.addRow(self.maskLabel, self.maskLine)
        self.form.addRow(self.histSizeLabel, self.histSizeLine)
        self.form.addRow(self.rangesLabel, self.rangesHLayout)
        self.form.addRow(self.accumulateLabel, self.accumulateBox)
        self.form.addRow(self.equalLabel, self.equalBox)

        layout.addLayout(self.form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def getData(self):
        return self.channelsLine.text(), self.maskLine.text(), self.histSizeLine.text(), \
               self.rangeStartLine.text(), self.rangeEndLine.text(), self.accumulateBox.isChecked(), \
               self.equalBox.isChecked()

    def importImage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "上传眼膜图像", "", "All Files(*)")
        self.maskLine.setText(imgName)
