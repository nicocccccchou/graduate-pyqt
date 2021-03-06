import os
import sys
import threading

import numpy as np
import cv2
import huicui
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from huicui import Image, Contour
from huicui.lib import helper
from huicui.operation import ImgOperation, ImgSample

from helperPackage.affineTransformMatrixDialog import AffineTransformMatrixDialog
from helperPackage.perspectiveTransformMatrixDialog import PerspectiveTransformMatrixDialog
from helperPackage.structuringElementDialog import StructuringElementDialog
from operationPackage.contourSelectDialog import ContourSelectDialog
from operationPackage.foregroundExtractionDialog import ForegroundExtractionDialog
from operationPackage.FourierTFDialog import FourierTFDialog
from operationPackage.geometricTFDialog import GeometricTFDialog
from operationPackage.histDialog import HistDialog
from helperPackage.rotationMatrix2DDialog import RotationMatrix2DDialog
from operationPackage.segmentationDialog import SegmentationDialog
from operationPackage.addDialog import AddDialog
from operationPackage.cannyDialog import CannyDialog
from helperPackage.commonHelper import CommonHelper
from operationPackage.contoursDialog import ContoursDialog
from operationPackage.gradientDialog import GradientDialog
from operationPackage.houghTFDialog import HoughTFDialog
from operationPackage.logicDialog import LogicDialog
from operationPackage.matchTemplateDialog import MatchTemplateDialog
from operationPackage.morphDialog import morphDialog
from operationPackage.samplingDialog import samplingDialog
from operationPackage.smoothDialog import SmoothDialog
from operationPackage.thresholdDialog import ThresholdDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):
    isClose = False
    isCapture = False
    num = 1
    selection = True
    currentIndex = 0
    LaplacianSample = []

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.cwd = os.getcwd()
        self.imageList = [Image()]
        self.image = Image()
        self.imageOperation = ImgOperation(copy=False)
        self.imgSample = ImgSample()
        self.contours = None
        self.channelMat = []
        self.initUI()

    def initUI(self):

        self.resize(1500, 700)
        self.setWindowTitle("?????????????????????????????????")
        self.center()

        """
        ?????????????????????
        """
        projectBar = self.menuBar()
        projectFile = projectBar.addMenu("??????")
        projectFile.addAction("????????????")
        projectFile.addAction("????????????")
        projectFile.addAction("????????????")
        projectFile.triggered[QAction].connect(self.projectAction)

        operationBar = self.menuBar()
        operationFile = operationBar.addMenu("????????????")
        singleImageOperationMenu = operationFile.addMenu("???????????????")
        multiImageOperationMenu = operationFile.addMenu("???????????????")

        grayTF = singleImageOperationMenu.addMenu("????????????")
        grayTF.addAction("??????????????????")
        grayTF.addAction("??????????????????")
        threshMenu = singleImageOperationMenu.addMenu("????????????")
        threshMenu.addAction("?????????????????????")
        threshMenu.addAction("?????????????????????")
        smoothMenu = singleImageOperationMenu.addMenu("????????????")
        smoothMenu.addAction("??????")
        smoothMenu.addAction("2D??????")
        singleImageOperationMenu.addAction("????????????")
        houghMenu = singleImageOperationMenu.addMenu("????????????")
        houghMenu.addAction("??????????????????")
        houghMenu.addAction("??????????????????")
        singleImageOperationMenu.addAction("????????????")  ##????????????

        addMenu = multiImageOperationMenu.addMenu("?????????????????????")
        addMenu.addAction("???????????????")
        addMenu.addAction("???????????????")
        multiImageOperationMenu.addAction("????????????")
        geometricTFMenu = multiImageOperationMenu.addMenu("????????????")
        geometricTFMenu.addAction("??????????????????")
        geometricTFMenu.addAction("???????????????")
        multiImageOperationMenu.addAction("???????????????")
        multiImageOperationMenu.addAction("????????????")
        multiImageOperationMenu.addAction("????????????")
        multiImageOperationMenu.addAction("????????????")
        multiImageOperationMenu.addAction("????????????")
        multiImageOperationMenu.addAction("??????????????????")  ##????????????
        multiImageOperationMenu.addAction("???????????????")
        multiImageOperationMenu.addAction("????????????")
        multiImageOperationMenu.addAction("????????????")
        operationFile.triggered[QAction].connect(self.operationAction)

        HelpBar = self.menuBar()
        HelpFile = HelpBar.addMenu("??????")
        HelpFile.addAction("????????????????????????")
        HelpFile.addAction("??????????????????")
        HelpFile.addAction("??????????????????")
        HelpFile.addAction("????????????????????????")

        HelpFile.triggered[QAction].connect(self.helpAction)

        """
        ??????layout???????????????
        """
        self.vLayout = QVBoxLayout(self)

        """
        ??????????????????
        """

        self.headBox = QGroupBox(self)
        self.headHLayout = QHBoxLayout(self)

        self.openCamera = QPushButton(self)
        self.openCamera.setText("????????????")
        self.captureCamera = QPushButton(self)
        self.captureCamera.setText("????????????")
        self.cameraSet = QPushButton(self)
        self.cameraSet.setText("????????????")
        self.functionAdd = QPushButton(self)
        self.functionAdd.setText("????????????")
        self.functionAdd.setStyleSheet("width:80px; height:100px;")
        self.functionAdd.setProperty("name", "functionAdd")

        self.openCamera.clicked.connect(self.cameraOpen)
        self.captureCamera.clicked.connect(self.captureVideo)

        self.headHLayout.addWidget(self.openCamera)
        self.headHLayout.addWidget(self.captureCamera)
        self.headHLayout.addWidget(self.cameraSet)
        self.headHLayout.addWidget(self.functionAdd)
        self.headHLayout.addStretch()
        self.headBox.setGeometry(0, 0, 1500, 100)
        self.headBox.setLayout(self.headHLayout)
        self.headBox.setProperty("name", "headBox")
        # self.headBox.setStyleSheet("border-bottom:2px solid #0c0e11 ;")
        self.vLayout.addWidget(self.headBox)

        self.bottomLayout = QHBoxLayout(self)

        self.bottomLeftLayout = QVBoxLayout(self)
        self.functionBox = QGroupBox(self)
        self.functionHLayout = QHBoxLayout(self)
        self.projectCB = QComboBox(self)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.projectCB.setFont(font)
        self.projectCB.addItem("???????????????")
        # self.projectCB.setGeometry(10, 100, 120, 55)
        self.projectCB.currentIndexChanged.connect(self.selectionchange)
        self.projectCB.setProperty("name", "projectCB")
        self.functionHLayout.addWidget(self.projectCB)
        self.functionHLayout.addStretch()
        self.functionBox.setLayout(self.functionHLayout)
        self.functionBox.setGeometry(0, 100, 820, 55)
        self.functionBox.setProperty("name", "functionBox")

        self.bottomLeftLayout.addWidget(self.functionBox)

        self.videoWidget = QWidget(self)
        self.videoWidget.setGeometry(QtCore.QRect(0, 150, 820, 500))
        self.videoLayout = QVBoxLayout(self)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        plt.subplot(111)
        self.figure.patch.set_facecolor('#111111')

        self.canvas.draw()
        self.videoLayout.addWidget(self.canvas)
        self.videoWidget.setLayout(self.videoLayout)
        self.bottomLeftLayout.addWidget(self.videoWidget)
        self.bottomLayout.addLayout(self.bottomLeftLayout)

        self.bottomRightBox = QGroupBox(self)
        self.bottomRightLayout = QVBoxLayout(self)
        self.dataBox = QGroupBox(self)
        self.dataForm = QGridLayout(self)

        self.dataBox.setLayout(self.dataForm)
        self.bottomRightLayout.addWidget(self.dataBox)
        # self.relatedDataLabel = QLabel(self)
        # font = QtGui.QFont()
        # font.setPointSize(35)
        # self.relatedDataLabel.setFont(font)
        # self.relatedDataLabel.setText("??????????????????")
        # self.relatedDataLabel.setProperty("name", "relatedDataLabel")
        # self.relatedDataLabel.setStyleSheet("width:400px;height:300px")
        # self.relatedDataLabel.resize(400,300)
        # self.relatedDataLabel.setGeometry(QtCore.QRect(0, 200, 400, 300))
        # self.bottomRightLayout.addWidget(self.relatedDataLabel)
        # self.bottomRightLayout.setGeometry(QtCore.QRect(820, 100, 680, 555))
        self.dataWidget = QWidget(self)
        # self.dataWidget.setGeometry(QtCore.QRect(0, 150, 820, 500))
        self.dataLayout = QVBoxLayout(self)

        # self.dataFigure = plt.figure()
        # self.dataCanvas = FigureCanvas(self.dataFigure)
        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)
        #
        # plt.subplot(111)
        # self.dataFigure.patch.set_facecolor('#111111')

        # self.dataCanvas.draw()
        # self.dataLayout.addWidget(self.dataCanvas)
        self.dataWidget.setLayout(self.dataLayout)
        self.bottomRightLayout.addWidget(self.dataWidget)
        # self.bottomRightLayout.addStretch()
        self.bottomRightBox.setLayout(self.bottomRightLayout)
        self.bottomRightBox.setGeometry(820, 100, 680, 555)
        self.bottomRightBox.setProperty("name", "bottomRightBox")
        self.bottomLayout.addWidget(self.bottomRightBox)
        self.bottomLayout.addStretch()
        self.vLayout.addLayout(self.bottomLayout)
        self.vLayout.addStretch()
        # self.setLayout(self.vLayout)

    def center(self):
        """
        ???????????????????????????
        :return:
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def projectAction(self, q):
        """
        ???????????????????????????
        :param q:
        :return:
        """
        if q.text() == "????????????":
            self.image = Image()
            MainWindow.selection = False
            name = "???????????????" + str(MainWindow.num)
            self.projectCB.addItem(name)
            MainWindow.currentIndex = self.projectCB.findText(name)
            self.imageList.append(self.image)
            self.projectCB.setCurrentIndex(MainWindow.currentIndex)
            self.figure.clear()
            plt.subplot(111)
            self.figure.patch.set_facecolor('#111111')
            self.canvas.draw()

        elif q.text() == "????????????":
            print("??????")
            imgName, imgType = QFileDialog.getOpenFileName(self, "????????????", self.cwd, "*.jpg;;*.png;;All Files(*)")
            if imgName == "":
                return
            self.image = Image(fileName=imgName)
            start = imgName.rindex("/")
            end = imgName.rindex(".")
            name = imgName[start + 1:end]
            MainWindow.selection = False
            self.projectCB.addItem(name)
            MainWindow.currentIndex = self.projectCB.findText(name)
            self.imageList.append(self.image)
            self.projectCB.setCurrentIndex(MainWindow.currentIndex)
            self.displayImage()
        elif q.text() == "????????????":
            print("??????")
            savePath, savType = QFileDialog.getSaveFileName(self, "????????????", self.cwd, "*.jpg;;*.png;;All Files(*)")
            if savePath == "":
                return
            self.image.writeImg(savePath=savePath)
        # elif q.text() == "???????????????":
        #     MainWindow.isClose = False
        #     self.isCamera = True
        #     self.cap = cv2.VideoCapture(0)
        #     th = threading.Thread(target=self.Display)
        #     th.start()

        else:
            MainWindow.isClose = False
            self.isCamera = False
            imgName, imgType = QFileDialog.getOpenFileName(self, "????????????", self.cwd, "*.mp4;;*.avi;;All Files(*)")
            self.cap = cv2.VideoCapture(imgName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
            th = threading.Thread(target=self.Display)
            th.start()

    def helpAction(self, q):
        if q.text() == "????????????????????????":
            dialog = RotationMatrix2DDialog()
            result = dialog.exec_()
            if result == 0:
                return
            centerValLine, angleValLine, scaleLine, downloadLine = dialog.getData()
            print(centerValLine)
            center = np.fromstring(centerValLine[1:-1], sep=',')
            if is_number(angleValLine) and is_number(scaleLine):
                print(tuple(center))
                M = helper.getRotationMatrix2D(tuple(center), float(angleValLine), float(scaleLine))
                np.savetxt(downloadLine, M, fmt='%f',
                           delimiter=' ')

        elif q.text() == "??????????????????":
            dialog = AffineTransformMatrixDialog()
            result = dialog.exec_()
            if result == 0:
                return
            srcLine, dstLine, downloadLine = dialog.getData()

            pt1 = self.transform(srcLine, (3, 2))
            pt2 = self.transform(dstLine, (3, 2))

            M = helper.getAffineTransform(pt1, pt2)
            np.savetxt(downloadLine, M, fmt='%f', delimiter=' ')

        elif q.text() == "??????????????????":
            dialog = PerspectiveTransformMatrixDialog()
            result = dialog.exec_()
            if result == 0:
                return
            srcLine, dstLine, downloadLine = dialog.getData()

            pt1 = self.transform(srcLine, (4, 2))
            pt2 = self.transform(dstLine, (4, 2))

            M = helper.getPerspectiveTransform(pt1, pt2)
            np.savetxt(downloadLine, M, fmt='%f', delimiter=' ')

        elif q.text() == "????????????????????????":
            dialog = StructuringElementDialog()
            result = dialog.exec_()
            if result == 0:
                return
            shapeTypeCB, ksizeLine, downloadLine = dialog.getData()
            if shapeTypeCB == "MORPH_RECT":
                shapeType = huicui.MORPH_RECT
            elif shapeTypeCB == "MORPH_CROSS":
                shapeType = huicui.MORPH_CROSS
            else:
                shapeType = huicui.MORPH_ELLIPSE
            ksize = np.fromstring(ksizeLine[1:-1], sep=',')

            M = helper.getStructuringElement(shapeType, tuple(ksize))
            np.savetxt(downloadLine, M, fmt='%f', delimiter=' ')

    def operationAction(self, q):
        """
        ???????????????????????????
        :param q:
        :return:
        """
        try:
            frame = self.image.getMat()
        except Exception:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("??????????????????                  ")
            msg.setInformativeText("??????????????????????????????")
            msg.setWindowTitle("????????????")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if q.text() == "??????????????????":
            print("?????????????????????")
            if len(self.image.getMat().shape) == huicui.THREE_CHANNEL:
                self.channelMat = self.image.split()
            self.image.cvtColor(huicui.COLOR_BGR2GRAY, copy=False)
            self.imageList[MainWindow.currentIndex] = self.image
            self.displayImage()
        elif q.text() == "??????????????????":
            print("?????????????????????")
            if len(self.channelMat) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("??????????????????                  ")
                msg.setInformativeText("??????????????????????????????")
                msg.setWindowTitle("????????????")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            self.image = self.imageOperation.merge(self.channelMat)
            self.displayImage()
        elif q.text() == "?????????????????????":
            dialog = ThresholdDialog(self, flag=0)
            result = dialog.exec_()
            if result == 0:
                return
            threshType, globalThreshType, threshLine, maxValueLine = dialog.getForm()
            if threshType == "THRESH_BINARY":
                threshTypeValue = 0
            elif threshType == "THRESH_BINARY_INV":
                threshTypeValue = 1
            elif threshType == "THRESH_TRUNC":
                threshTypeValue = 2
            elif threshType == "THRESH_TOZERO":
                threshTypeValue = 3
            else:
                threshTypeValue = 4
            if globalThreshType == "    ":
                globalThreshTypeValue = 0
            elif globalThreshType == "THRESH_OTSU":
                if len(self.image.getMat().shape) == huicui.THREE_CHANNEL:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("?????????????????????????????????                  ")
                    msg.setInformativeText("??????????????????????????????????????????????????????")
                    msg.setWindowTitle("????????????")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
                globalThreshTypeValue = 8
            else:
                globalThreshTypeValue = 16
            if is_number(threshLine) and is_number(maxValueLine):
                self.image.threshold(float(threshLine), float(maxValueLine), threshTypeValue + globalThreshTypeValue,
                                     copy=False)
                self.displayImage()
        elif q.text() == "?????????????????????":
            dialog = ThresholdDialog(self, flag=1)
            result = dialog.exec_()
            if result == 0:
                return
            threshTypeCB, adaptiveMethodCB, blockSizeLine, CLine, maxValueLine = dialog.getForm()
            if threshTypeCB == "THRESH_BINARY":
                threshType = 0
            else:
                threshType = 1
            if adaptiveMethodCB == "ADAPTIVE_THRESH_GAUSSIAN_C":
                adaptiveMethod = 1
            else:
                adaptiveMethod = 0

            if is_number(blockSizeLine) and is_number(maxValueLine) and is_number(CLine):
                self.image.adaptiveThreshold(float(maxValueLine), adaptiveMethod, threshType, int(blockSizeLine),
                                             float(CLine), copy=False)
                self.displayImage()
        elif q.text() == "????????????":
            dialog = AddDialog(self, flag=1)
            result = dialog.exec_()
            if result == 0:
                return
            numberText = dialog.getData()
            if is_number(numberText):
                self.image.addNumber(float(numberText), copy=False)
                self.displayImage()
        elif q.text() == "???????????????":
            dialog = AddDialog(self, flag=2)
            result = dialog.exec_()
            if result == 0:
                return
            imgName = dialog.getData()
            img = Image(fileName=imgName)
            self.imageOperation.add(self.image, img)
            self.displayImage()
        elif q.text() == "???????????????":
            dialog = AddDialog(self, flag=3)
            result = dialog.exec_()
            if result == 0:
                return
            imgName, alphaText, betaText, gammaText = dialog.getData()
            if is_number(alphaText) and is_number(betaText) and is_number(gammaText):
                img = Image(fileName=imgName)
                alpha = float(alphaText)
                beta = float(betaText)
                gamma = float(gammaText)
                self.imageOperation.addWeighted(self.image, img, alpha=alpha, beta=beta, gamma=gamma)
                self.displayImage()
        elif q.text() == "??????":
            dialog = SmoothDialog(self, flag=0)
            result = dialog.exec_()
            if result == 0:
                return
            data = dialog.getData()
            if data[0] == "????????????":
                smoothType = huicui.SMOOTH_BLUR
                ksize = np.fromstring(data[1][1:-1], sep=',')
                self.image.smooth(tuple(ksize), smoothType, copy=False)
            elif data[0] == "????????????":
                smoothType = huicui.SMOOTH_BOXFILTER
                ksize = np.fromstring(data[1][1:-1], sep=',')
                if is_number(data[2]):
                    ddepth = int(data[2])
                    self.image.smooth(tuple(ksize), smoothType, ddepth=ddepth, copy=False)
            elif data[0] == "????????????":
                smoothType = huicui.SMOOTH_GAUSSIANBLUR
                ksize = np.fromstring(data[1][1:-1], sep=',')
                if data[2] == "":
                    sigmaX = 0
                else:
                    sigmaX = data[2]
                if data[3] == "":
                    sigmaY = 0
                else:
                    sigmaY = data[3]
                if is_number(sigmaX) and is_number(sigmaY):
                    self.image.smooth(tuple(ksize), smoothType, sigma1=float(sigmaX), sigma2=float(sigmaY), copy=False)
            elif data[0] == "????????????":
                smoothType = huicui.SMOOTH_MEDIANBLUR
                ksize = data[1]
                if is_number(ksize):
                    self.image.smooth(int(ksize), smoothType, copy=False)
            else:
                smoothType = huicui.SMOOTH_BILATERALFILTER
                d = data[1]
                if is_number(d):
                    d = int(d)
                if data[2] == "":
                    sigmaColor = 0
                else:
                    sigmaColor = data[2]
                if data[3] == "":
                    sigmaSpace = 0
                else:
                    sigmaSpace = data[3]
                if is_number(sigmaColor) and is_number(sigmaSpace):
                    self.image.smooth(d, smoothType, sigma1=float(sigmaColor), sigma2=float(sigmaSpace), copy=False)
            self.displayImage()
        elif q.text() == "2D??????":
            dialog = SmoothDialog(self, flag=1)
            result = dialog.exec_()
            if result == 0:
                return
            kernelPath = dialog.getData()
            if kernelPath == "":
                return
            kernel = np.loadtxt(kernelPath, delimiter=' ')
            kernel = kernel.astype(np.float32)
            print(kernelPath)
            # if is_number(deltaLine):
            self.image.filter2D(kernel, -1, copy=False)
            self.displayImage()
        elif q.text() == "????????????":
            dialog = LogicDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            logicTypeCB, imageLine, = dialog.getData()
            if logicTypeCB == "BITWISE_AND":
                logicType = huicui.BITWISE_AND
                image2 = Image(fileName=imageLine)
                self.imageOperation.bitwise(self.image, image2, logicType)
            elif logicTypeCB == "BITWISE_OR":
                logicType = huicui.BITWISE_OR
                image2 = Image(fileName=imageLine)
                self.imageOperation.bitwise(self.image, image2, logicType)
            elif logicTypeCB == "BITWISE_NOT":
                logicType = huicui.BITWISE_NOT
                self.imageOperation.bitwise(self.image, None, logicType)
            else:
                logicType = huicui.BITWISE_XOR
                image2 = Image(fileName=imageLine)
                self.imageOperation.bitwise(self.image, image2, logicType)
            self.displayImage()
        elif q.text() == "??????????????????":
            dialog = GeometricTFDialog(self, flag=0)
            result = dialog.exec_()
            if result == 0:
                return
            data = dialog.getData()
            if data[0] == "??????":
                geometricTF_type = huicui.GEOMETRICTF_RESIZE
                ksize = np.fromstring(data[1][1:-1], sep=',')
                self.imageOperation.simpleGeometricTF(geometricTF_type, self.image, tuple(ksize))
                self.displayImage()
            elif data[0] == "??????":
                geometricTF_type = huicui.GEOMETRICTF_FLIP
                flipCodeCB = data[1]
                if flipCodeCB == "???x?????????":
                    flipCode = 0
                elif flipCodeCB == "???y?????????":
                    flipCode = 1
                else:
                    flipCode = -1
                self.imageOperation.simpleGeometricTF(geometricTF_type, self.image, flipCode=flipCode)
                self.displayImage()
            elif data[0] == "??????":
                geometricTF_type = huicui.GEOMETRICTF_WARPAFFINE

                ksize = np.fromstring(data[1][1:-1], sep=',')
                if data[2] is True:
                    pt1 = data[3]
                    pt2 = data[4]
                    pt1 = self.transform(pt1, (3, 2))
                    pt2 = self.transform(pt2, (3, 2))
                    M = helper.getAffineTransform(pt1, pt2)
                else:
                    M = np.loadtxt(data[3], delimiter=' ')
                ksize = ksize.astype(np.float32)
                self.imageOperation.simpleGeometricTF(geometricTF_type, self.image, tuple(ksize), M=M)
                self.displayImage()
            else:
                geometricTF_type = huicui.GEOMETRICTF_WARPPERSPECTIVE
                ksize = np.fromstring(data[1][1:-1], sep=',')
                ksize = ksize.astype(np.float32)
                if data[2] is True:
                    pt1 = data[3]
                    pt2 = data[4]
                    pt1 = self.transform(pt1, (4, 2))
                    pt2 = self.transform(pt2, (4, 2))
                    M = helper.getPerspectiveTransform(pt1, pt2)
                else:
                    M = np.loadtxt(data[2], delimiter=' ')
                self.imageOperation.simpleGeometricTF(geometricTF_type, self.image, tuple(ksize), M=M)
                self.displayImage()
        elif q.text() == "???????????????":
            dialog = GeometricTFDialog(self, flag=1)
            result = dialog.exec_()
            if result == 0:
                return
            mapXLine, mapYLine, interpolationTypeCB = dialog.getData()
            if interpolationTypeCB == "INTER_NEAREST":
                interpolationType = huicui.INTER_NEAREST
            elif interpolationTypeCB == "INTER_LINEAR":
                interpolationType = huicui.INTER_LINEAR
            elif interpolationTypeCB == "INTER_CUBIC":
                interpolationType = huicui.INTER_CUBIC
            elif interpolationTypeCB == "INTER_LANCZOS4":
                interpolationType = huicui.INTER_LANCZOS4
            elif interpolationTypeCB == "INTER_LINEAR_EXACT":
                interpolationType = huicui.INTER_LINEAR_EXACT
            elif interpolationTypeCB == "WARP_FILL_OUTLIERS":
                interpolationType = huicui.WARP_FILL_OUTLIERS
            else:
                interpolationType = huicui.WARP_INVERSE_MAP
            mapX = np.loadtxt(mapXLine, delimiter=' ')
            mapY = np.loadtxt(mapYLine, delimiter=' ')
            mapX = mapX.astype(np.float32)
            mapY = mapY.astype(np.float32)
            self.imageOperation.remap(self.image, mapX, mapY, interpolationType)
            self.displayImage()
        elif q.text() == "???????????????":
            dialog = morphDialog(self)
            result = dialog.exec_()
            if result == 0:
                return

            data = dialog.getData()
            morphType = data[0]
            iterationsLine = data[1]

            if is_number(iterationsLine):
                if morphType == "MORPH_ERODE":
                    morph = huicui.MORPH_ERODE
                elif morphType == "MORPH_DILATE":
                    morph = huicui.MORPH_DILATE
                elif morphType == "MORPH_OPEN":
                    morph = huicui.MORPH_OPEN
                elif morphType == "MORPH_CLOSE":
                    morph = huicui.MORPH_CLOSE
                elif morphType == "MORPH_GRADIENT":
                    morph = huicui.MORPH_GRADIENT
                elif morphType == "MORPH_TOPHAT":
                    morph = huicui.MORPH_TOPHAT
                elif morphType == "MORPH_BLACKHAT":
                    morph = huicui.MORPH_BLACKHAT
                else:
                    morph = huicui.MORPH_HITMISS
                """
                    ?????????????????????????????????
                """
                if data[2] is False:
                    kernelPath = data[3]
                    M = np.loadtxt(kernelPath, delimiter=' ')
                    M = M.astype(np.uint8)
                else:
                    shapeTypeCB = data[3]
                    ksizeLine = data[4]
                    if shapeTypeCB == "MORPH_RECT":
                        shapeType = huicui.MORPH_RECT
                    elif shapeTypeCB == "MORPH_CROSS":
                        shapeType = huicui.MORPH_CROSS
                    else:
                        shapeType = huicui.MORPH_ELLIPSE
                    ksize = np.fromstring(ksizeLine[1:-1], sep=',')

                    M = helper.getStructuringElement(shapeType, tuple(ksize))
                self.imageOperation.morphologyEx(morph, self.image, M, iterations=int(iterationsLine))
                self.displayImage()
        elif q.text() == "????????????":
            dialog = CannyDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            minThreshValLine, maxThreshValLine, apertureSizeLine = dialog.getData()
            if is_number(minThreshValLine) and is_number(maxThreshValLine) and is_number(apertureSizeLine):
                self.imageOperation.canny(self.image, float(minThreshValLine), float(maxThreshValLine),
                                          float(apertureSizeLine))
                self.displayImage()
        elif q.text() == "????????????":
            if len(MainWindow.LaplacianSample) == 0:
                dialog = samplingDialog(self, flag=False)
            else:
                dialog = samplingDialog(self, flag=True)
            result = dialog.exec_()
            if result == 0:
                return
            data = dialog.getData()
            if data[0] == "????????????":
                iterationLine = data[1]
                isLaplacianButton = data[2]
                if is_number(iterationLine):
                    LaplacianSample, image = self.imgSample.pyrDown(self.image, int(iterationLine), isLaplacianButton)
                    self.image = image
                    self.LaplacianSample.append(LaplacianSample)
            else:
                if len(MainWindow.LaplacianSample) == 0:
                    iterationLine = data[1]
                    isLaplacian = data[2]
                    if is_number(iterationLine):
                        image = self.imgSample.pyrUp(self.image, int(iterationLine), isLaplacian,
                                                     LaplacianSample=self.LaplacianSample)
                        if isLaplacian:
                            for i in range(int(iterationLine)):
                                self.LaplacianSample.pop()
                        self.image = image
                else:
                    iterationLine = data[1]
                    if is_number(iterationLine):
                        image = self.imgSample.pyrUp(self.image, int(iterationLine))
                        self.image = image
            self.displayImage()

        elif q.text() == "????????????":
            dialog = ContoursDialog(self)
            # dialog._signal.connect(self.slotShowTransThreadStatus)
            result = dialog.exec_()

            if result == 0:
                return
            data = dialog.getData()
            if data[1] == "RETR_CCOMP":
                mode = huicui.RETR_CCOMP
            elif data[1] == "RETR_EXTERNAL":
                mode = huicui.RETR_EXTERNAL
            elif data[1] == "RETR_LIST":
                mode = huicui.RETR_LIST
            elif data[1] == "RETR_TREE":
                mode = huicui.RETR_TREE
            else:
                mode = huicui.RETR_FLOODFILL

            if data[2] == "CHAIN_APPROX_NONE":
                method = huicui.CHAIN_APPROX_NONE
            elif data[2] == "CHAIN_APPROX_SIMPLE":
                method = huicui.CHAIN_APPROX_SIMPLE
            elif data[2] == "CHAIN_APPROX_TC89_KCOS":
                method = huicui.CHAIN_APPROX_TC89_KCOS
            else:
                method = huicui.CHAIN_APPROX_TC89_L1
            # print(len(data))
            if data[0] is True:

                if data[3] == "THRESH_BINARY":
                    thresholdType = huicui.THRESH_BINARY
                elif data[3] == "THRESH_BINARY_INV":
                    thresholdType = huicui.THRESH_BINARY_INV
                elif data[3] == "THRESH_TRUNC":
                    thresholdType = huicui.THRESH_TRUNC
                elif data[3] == "THRESH_TOZERO":
                    thresholdType = huicui.THRESH_TOZERO
                else:
                    thresholdType = huicui.THRESH_TOZERO_INV

                if data[4] == "    ":
                    globalThreshold = 0
                elif data[4] == "THRESH_OTSU":
                    globalThreshold = huicui.THRESH_OTSU
                else:
                    globalThreshold = huicui.THRESH_TRIANGLE
                threshLine = data[5]
                maxValueLine = data[6]
                if is_number(threshLine) and is_number(maxValueLine):
                    contours, hierarchy = self.imageOperation.findContours(self.image, mode, method,
                                                                           thresh=float(threshLine),
                                                                           maxval=float(maxValueLine),
                                                                           type=thresholdType + globalThreshold,
                                                                           threshold=True)
            else:
                contours, hierarchy = self.imageOperation.findContours(self.image, mode, method, threshold=False)
            self.contours = contours
            contourDialog = ContourSelectDialog(self, contourLen=len(contours))
            contourDialog._signal.connect(self.previewContour)
            result = contourDialog.exec_()
            if result == 0:
                return
            contourIndex = contourDialog.getData()
            contour = Contour(img=self.image, contour=self.contours[contourIndex])
            image = contour.drawContour(color=(255, 255, 255), thickness=5)
            self.image = image
            self.displayImage()
        elif q.text() == "??????????????????":
            dialog = HistDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            channelsLine, maskLine, histSizeLine, rangeStartLine, rangeEndLine, accumulate, equal = dialog.getData()
            if maskLine != "":
                maskImage = Image(fileName=maskLine)
            else:
                maskImage = None
            if is_number(channelsLine) and is_number(histSizeLine) and is_number(rangeStartLine) and is_number(
                    rangeEndLine):
                hist = self.imageOperation.calcHist(self.image, int(channelsLine), int(histSizeLine),
                                                    (int(rangeStartLine), int(rangeEndLine)), mask=maskImage,
                                                    accumulate=accumulate, equal=equal)
                print(hist)
        elif q.text() == "???????????????":
            dialog = FourierTFDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            maskPath = dialog.getData()
            maskImg = Image(fileName=maskPath, flag=0)
            mask = self.imageOperation.merge([maskImg.getMat(), maskImg.getMat()])
            # plt.subplot(121)
            # plt.imshow(self.image.getMat(), cmap="gray")
            # print(1)
            self.imageOperation.filter(self.image, mask)

            self.displayImage()

            print(1)
        elif q.text() == "????????????":
            dialog = MatchTemplateDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            templatePath, methodCB = dialog.getData()
            if methodCB == "TM_SQDIFF":
                method = huicui.TM_SQDIFF
            elif methodCB == "TM_SQDIFF_NORMED":
                method = huicui.TM_SQDIFF_NORMED
            elif methodCB == "TM_CCORR":
                method = huicui.TM_CCORR
            elif methodCB == "TM_CCORR_NORMED":
                method = huicui.TM_CCORR_NORMED
            elif methodCB == "TM_CCOEFF":
                method = huicui.TM_CCOEFF
            else:
                method = huicui.TM_CCOEFF_NORMED
            image = Image(fileName=templatePath)
            rst = self.image.matchTemplate(image, method)
            print(rst)
        elif q.text() == "??????????????????":
            if len(self.image.getMat().shape) == huicui.THREE_CHANNEL:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("?????????????????????????????????                  ")
                msg.setInformativeText("????????????????????????????????????????????????????????????")
                msg.setWindowTitle("????????????")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            dialog = HoughTFDialog(self, flag=0)
            result = dialog.exec_()
            if result == 0:
                return
            rhoLine, thetaLine, thresholdLine, optimizeButton, minLineLengthLine, maxLineGapLine = dialog.getData()
            if is_number(rhoLine) and is_number(thetaLine) and is_number(thresholdLine) and is_number(
                    minLineLengthLine) and is_number(maxLineGapLine):
                lines = self.image.HoughLine(int(thresholdLine), float(minLineLengthLine), float(maxLineGapLine),
                                            float(rhoLine), np.pi / 180, optimizeButton)
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    helper.draw(self.image,(x1,y1),(x2,y2),(255,255,255),5,drawType=huicui.DRAW_LINE,iscopy=False)
                self.displayImage()
        elif q.text() == "??????????????????":
            if len(self.image.getMat().shape) == huicui.THREE_CHANNEL:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("?????????????????????????????????                  ")
                msg.setInformativeText("????????????????????????????????????????????????????????????")
                msg.setWindowTitle("????????????")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            dialog = HoughTFDialog(self, flag=1)
            result = dialog.exec_()
            if result == 0:
                return
            dpLine, minDistLine, param1Line, param2Line, minRadiusLine, maxRadiusLine = dialog.getData()
            if is_number(dpLine) and is_number(minDistLine) and is_number(param1Line) and is_number(
                    param2Line) and is_number(minRadiusLine) and is_number(maxRadiusLine):
                circles = self.image.HoughCircle(huicui.HOUGH_GRADIENT, float(dpLine), float(minDistLine),
                                                 float(param1Line), float(param2Line), int(minRadiusLine),
                                                 int(maxRadiusLine))
                print(circles)
                if circles is None:
                    return
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    helper.draw(self.image,(i[0],i[1]),i[2],(255,255,255),12,huicui.DRAW_CIRCLE,iscopy=False)
                self.displayImage()
        elif q.text() == "????????????":
            dialog = SegmentationDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            distanceTypeCB, maskSizeCB, thresholdRatioLine, kernelPath, openIterationsLine, dilateIterationsLine = dialog.getData()
            if distanceTypeCB == "DIST_L1":
                distanceType = huicui.DIST_L1
            elif distanceTypeCB == "DIST_L2":
                distanceType = huicui.DIST_L2
            elif distanceTypeCB == "DIST_C":
                distanceType = huicui.DIST_C
            elif distanceTypeCB == "DIST_L12":
                distanceType = huicui.DIST_L12
            elif distanceTypeCB == "DIST_FAIR":
                distanceType = huicui.DIST_FAIR
            elif distanceTypeCB == "DIST_WELSCH":
                distanceType = huicui.DIST_WELSCH
            else:
                distanceType = huicui.DIST_HUBER
            if maskSizeCB == "DIST_MASK_3":
                maskSize = huicui.DIST_MASK_3
            elif maskSizeCB == "DIST_MASK_5":
                maskSize = huicui.DIST_MASK_5
            else:
                maskSize = huicui.DIST_MASK_PRECISE
            if is_number(thresholdRatioLine) and is_number(openIterationsLine) and is_number(dilateIterationsLine):
                kernel = np.loadtxt(kernelPath, delimiter=' ')
                self.imageOperation.imageSegmentation(self.image, distanceType, maskSize, float(thresholdRatioLine),
                                                      kernel, int(openIterationsLine), int(dilateIterationsLine))
                self.displayImage()
        elif q.text() == "????????????":
            dialog = ForegroundExtractionDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            maskPath, rectLine, iterCountLine = dialog.getData()
            maskImg = Image(fileName=maskPath)
            rect = np.fromstring(rectLine[1:-1], sep=',')
            if is_number(iterCountLine):
                self.imageOperation.GrabCut(self.image, maskImg, rect, int(iterCountLine))
                self.displayImage()
        elif q.text() == "????????????":
            dialog = GradientDialog(self)
            result = dialog.exec_()
            if result == 0:
                return
            gradientTypeCB, ddepthCB, dxLine, dyLine = dialog.getData()
            if gradientTypeCB == "Sobel??????":
                gradientType = huicui.GRADIENT_SOBEL
            elif gradientTypeCB == "Scharr??????":
                gradientType = huicui.GRADIENT_SCHARR
            else:
                gradientType = huicui.GRADIENT_LAPLACIAN
            if ddepthCB == "CV_8U":
                ddepth = huicui.CV_8U
            elif ddepthCB == "CV_16U":
                ddepth = huicui.CV_16U
            elif ddepthCB == "CV_32F":
                ddepth = huicui.CV_32F
            else:
                ddepth = huicui.CV_64F
            if is_number(dxLine) and is_number(dyLine):
                self.imageOperation.gradient(gradientType, self.image, ddepth, int(dxLine), int(dyLine))
                self.displayImage()
        else:
            print("?????????")
            pass

    def cameraOpen(self):
        """
        ???????????????
        :return:
        """
        MainWindow.isClose = False
        self.isCamera = True
        self.cap = cv2.VideoCapture(0)
        self.Display()
        # th = threading.Thread(target=self.Display)
        # th.start()

    def captureVideo(self):
        """
        ?????????????????????
        :return:
        """
        MainWindow.isCapture = True

    def closeCamera(self):
        """
        ??????/???????????????
        :return:
        """
        if MainWindow.isClose is False:
            self.closeButton.setText("????????????")
            MainWindow.isClose = True
        else:
            self.closeButton.setText("????????????")
            MainWindow.isClose = False

    def Display(self):
        """
        ????????????
        :return:
        """
        self.figure.clear()
        plt.subplot(111)
        while self.cap.isOpened():
            success, frame = self.cap.read()
            # RGB???BGR
            if success:

                # frameCopy = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # img = QImage(frameCopy.data, frameCopy.shape[1], frameCopy.shape[0], QImage.Format_RGB888)
                # self.videoLabel.setPixmap(QPixmap.fromImage(img).scaled(800, 500))

                # plt.imshow(frameCopy)
                # plt.axis('off')
                # self.canvas.draw()
                # time.sleep(0.01)
                cv2.imshow('frame', frame)

                if self.isCamera:
                    c = cv2.waitKey(1)
                    if c == 27:
                        break
                else:
                    cv2.waitKey(int(1000 / self.frameRate))
                if MainWindow.isCapture is True:
                    self.image.setAttr(mat=frame)
                    self.imageList[MainWindow.currentIndex] = self.image

                    frameCopy = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    plt.imshow(frameCopy)
                    plt.axis('off')
                    self.canvas.draw()

                    MainWindow.isCapture = False
                    break
            # ?????????????????????????????????
            if MainWindow.isClose is True:
                # ??????????????????????????????????????????label
                print("?????????????????????")
                # self.stopEvent.clear()
                # self.ui.DispalyLabel.clear()
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def selectionchange(self, index):
        """
        ComboBox??????????????????????????????
        :param index:
        :return:
        """
        MainWindow.currentIndex = index
        if MainWindow.selection is False:
            MainWindow.selection = True
            return
        image = self.imageList[index]
        self.image = image
        self.displayImage()

    def displayImage(self):
        try:
            frame = self.image.getMat()

            if len(frame.shape) == huicui.THREE_CHANNEL:
                imageCopy = self.image.cvtColor(huicui.COLOR_BGR2RGB)
                frame = imageCopy.getMat()
                plt.imshow(frame)
            else:
                plt.imshow(frame, cmap='gray')

            plt.axis('off')
            self.canvas.draw()
        except Exception:

            self.figure.clear()
            plt.subplot(111)
            self.figure.patch.set_facecolor('#111111')
            self.canvas.draw()

    def transform(self, data, shape):
        data = data.replace("[", ",")
        data = data.replace("]", ",")
        datalist = data.split(",")
        while "" in datalist:
            datalist.remove("")
        x = np.array(datalist, dtype=np.float32)
        x = x.reshape(shape)
        return x

    def previewContour(self, contourIndex):
        contour = Contour(img=self.image, contour=self.contours[contourIndex])
        image = contour.drawContour(color=(255, 255, 255), thickness=5)
        image.showImg("contourDemo")
        helper.waitKey()


def is_number(s):
    """
    ???????????????
    :param s:
    :return:
    """
    try:
        float(s)
        return True
    except ValueError:
        pass

    return False


def main():
    app = QApplication(sys.argv)
    qssStyle = CommonHelper.readQSS('/Users/zhoujiahao/Downloads/graduate/VisualPlatform/style.qss')
    ex = MainWindow()

    ex.setStyleSheet(qssStyle)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
