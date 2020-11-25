import sys
import cv2
from pyxelate import Pyxelate
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets, uic

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('ui/main.ui', self)

        '''Find Children'''
        # layouts
        # self.layout_: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'layout_')
        self.hlayout_top: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'hlayout_top')
        self.hlayout_body: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'hlayout_body')
        self.hlayout_bottom: QtWidgets.QLayout = self.findChild(QtWidgets.QLayout, 'hlayout_bottom')

        # Scrollareas
        self.scrollarea_input: QtWidgets.QScrollArea = self.findChild(QtWidgets.QScrollArea, 'scrollarea_input')
        self.scrollarea_output: QtWidgets.QScrollArea = self.findChild(QtWidgets.QScrollArea, 'scrollarea_output')

        # labels
        # self.lbl_: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_')
        self.lbl_input: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_input')
        self.lbl_output: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_output')
        self.lbl_factor: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_factor')
        self.lbl_color: QtWidgets.QLabel = self.findChild(QtWidgets.QLabel, 'lbl_color')

        # buttons
        # self.btn_: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_') #use this for template
        self.btn_open: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_open')
        self.btn_pyxelate: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_pyxelate')
        self.btn_adjustment: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_adjustment')
        self.btn_effect: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, 'btn_effect')


        # self.menuFile = self.findChild(QtWidgets.)
        # self.menuABout = self.findChild(QtWidgets.)

        #checkboxes
        # self.checkbox_ : QtWidgets.QCheckBox = self.findChild(QtWidgets.QCheckBox, 'checkbox_')
        self.checkbox_dither: QtWidgets.QCheckBox = self.findChild(QtWidgets.QCheckBox, 'checkbox_dither')
        self.checkbox_fit: QtWidgets.QCheckBox = self.findChild(QtWidgets.QCheckBox, 'checkbox_fit')
        # spinboxes
        self.spinbox_factor: QtWidgets.QSpinBox = self.findChild(QtWidgets.QSpinBox, 'spinbox_factor')
        self.spinbox_color: QtWidgets.QSpinBox = self.findChild(QtWidgets.QSpinBox, 'spinbox_color')
        self.spinbox_zoom: QtWidgets.QSpinBox = self.findChild(QtWidgets.QSpinBox, 'spinbox_zoom')

        # sliders
        self.hslider_zoom: QtWidgets.QSlider = self.findChild(QtWidgets.QSlider, 'hslider_zoom')

        # actions
        self.actionOpen: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionOpen')
        self.actionSave: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionSave')
        self.actionExit: QtWidgets.QAction = self.findChild(QtWidgets.QAction, 'actionExit')
        '''end findChildren'''

        '''Connection'''
        # is_clicked
        # self.btn_.clicked.connect(lambda: self.isClicked('btn_'))
        self.btn_open.clicked.connect(lambda: self.isClicked('open'))
        self.btn_pyxelate.clicked.connect(lambda: self.isClicked('apply'))
        self.btn_adjustment.clicked.connect(lambda: self.isClicked('adjustments'))
        self.btn_effect.clicked.connect(lambda: self.isClicked('effects'))

        # buttons
        # self.btn_pyxelate.clicked.connect(self.test_combobox)
        self.btn_open.clicked.connect(self.openImage)
        self.btn_pyxelate.clicked.connect(self.pyxelate)
        self.checkbox_fit.clicked.connect(self.switchView)


        # spinboxes
        #self.spinbox_zoom.valueChanged.connect(lambda: self.scaleImage(self.spinbox_zoom.value()/100))

        # hsliders
        #self.hslider_zoom.valueChanged.connect(lambda: self.scaleImage(self.hslider_zoom.value()/100))

        # actions
        self.actionOpen.triggered.connect(self.openImage)
        self.actionSave.triggered.connect(self.saveImage)
        '''end Connection'''

        '''preloaded'''
        self.scale_factor = 1.0
        #self.is_fittoframe = False
        self.input_image = None
        self.output_image = None

        self.show()

    def isClicked(self, obj: str):
        '''
		Check if the object is clicked, result is printed in the console
		:param obj: the name of the object, in string
		:return: None
		'''
        print("{} was clicked".format(obj))

    def openImage(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', '', 'Image files (*.png *.xpm *.jpg *.tif)')
        # print(filename)
        print(file_path)
        if file_path != '' and file_path != None:
            #self.path = image_path
            #self.cv_image = cv2.imread(image_path)
            #self.backup_image = QtGui.QPixmap(self.convertMatToQImage(self.cv_image))
            #self.showImage(self.lbl_input, self.cv_image)
            self.input_image = QtGui.QPixmap(file_path)
            self.lbl_input.setPixmap(self.input_image)
            self.resizeImage()
        else:
            print("invalid file")

    def saveImage(self):
        if self.lbl_output.pixmap() is not None:
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "untitled.png",
                                                      "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

            if file_path == "":
                return
            self.lbl_output.pixmap().save(file_path)

    def showImage(self, label: QtWidgets.QLabel, cv_img=None):
        if cv_img is not None:
            image = self.convertMatToQImage(cv_img)
            image = QtGui.QPixmap(image)
            label.setPixmap(image)
        else:
            print("Warning: self.cv_image is empty.")

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.resizeImage()
        #self.update()

    def resizeImage(self):
        if self.input_image is not None:
            if self.checkbox_fit.isChecked():
                #width = min(self.input_image.width(), self.scrollarea_input.width()-21)
                #height = min(self.input_image.height(), self.scrollarea_input.height()-10)
                width = self.scrollarea_input.width()-21
                height = self.scrollarea_input.height()-10
                self.lbl_input.setPixmap(self.input_image.scaled(width, height, QtCore.Qt.KeepAspectRatio))
                print(width, height)
                if self.output_image is not None:
                    self.lbl_output.setPixmap(self.output_image.scaled(width,height,QtCore.Qt.KeepAspectRatio))

    def resetImage(self):
        if self.input_image is not None:
            self.lbl_input.setPixmap(self.input_image)
            if self.output_image is not None:
                self.lbl_input.setPixmap(self.output_image)

    def switchView(self):
        if self.checkbox_fit.isChecked():
            self.resizeImage()
        else:
            self.resetImage()

    def pyxelate(self):
        if self.input_image is not None:
            img = self.convertQImageToMat(self.input_image)

            # generate pixel art that is 1/14 the size

            height, width, _ = img.shape

            factor = self.spinbox_factor.value()
            colors = self.spinbox_color.value()
            dither = self.checkbox_dither.isChecked()

            print(img.shape)

            p = Pyxelate(height // factor, width // factor, colors, dither)
            img_small = p.convert(img)  # convert an image with these settings

            qimage = self.convertMatToQImage(img_small)
            self.output_image = QtGui.QPixmap.fromImage(qimage)
            self.lbl_output.setPixmap(self.output_image)
            self.resizeImage()

            #_, axes = plt.subplots(1, 2, figsize=(16, 16))
            #axes[0].imshow(img)
            #axes[1].imshow(img_small)
            #plt.show()

            pass

    def convertMatToQImage(self, mat: np.ndarray=None):
        if mat is not None:
            height, width = mat.shape[:2]
            bytes_per_line = 3 * width
            image = QtGui.QImage(mat.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            return image

    def convertQImageToMat(self, pixmap = None):
        '''  Converts a QImage into an opencv MAT format  '''
        if pixmap is not None:
            if type(pixmap) is QtGui.QPixmap:
                new_qimage = pixmap.toImage().convertToFormat(QtGui.QImage.Format_RGBA8888)

            width = new_qimage.width()
            height = new_qimage.height()

            ptr = new_qimage.bits()
            ptr.setsize(new_qimage.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
            arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
            return arr

    # def scaleImage(self, factor):
    #     self.scale_factor *= factor
    #     self.lbl_input.resize(self.scale_factor * self.lbl_input.pixmap().size())
    #
    #     self.adjustScrollBar(self.scrollarea_input.horizontalScrollBar(), factor)
    #     self.adjustScrollBar(self.scrollarea_input.verticalScrollBar(), factor)
    #
    #     print(factor)
    #
    # def adjustScrollBar(self, scrollbar, factor):
    #     scrollbar.setValue(int(factor * scrollbar.value() + ((factor - 1) * scrollbar.pageStep() / 2)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = Ui_MainWindow()
    app.exec_()
