import sys
from math import ceil
import re
import pytesseract

from PyQt5 import QtCore, QtGui, QtWidgets

from PIL import Image, ImageGrab
import PIL.ImageOps


def change_widget_colour(widget, colour):
    p = widget.palette()
    p.setColor(widget.backgroundRole(), colour)
    widget.setPalette(p)


class mymainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        # Setting up overlay settings
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
            )
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
            QtCore.QSize(64, 64),
            QtWidgets.qApp.desktop().availableGeometry()))        
        
        # Creating label
        self.label = QtWidgets.QLabel(self)
        self.label.move(16,16)
        self.label.setStyleSheet("font: 18pt Helvetica; color: black;")
        change_widget_colour(self, QtCore.Qt.red)

        self.image = None
        self.BB_top_left = None
        self.BB_top_right = None
        
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F2:
            if not self.BB_top_right:
                change_widget_colour(self, QtCore.Qt.yellow)
            else:
                change_widget_colour(self, QtCore.Qt.green)
            cursor = QtGui.QCursor()
            self.BB_top_left = cursor.pos().x(), cursor.pos().y()
        if event.key() == QtCore.Qt.Key_F3:
            if not self.BB_top_left:
                change_widget_colour(self, QtCore.Qt.yellow)
            else:
                change_widget_colour(self, QtCore.Qt.green)
            cursor = QtGui.QCursor()
            self.BB_top_right = cursor.pos().x(), cursor.pos().y()
        if event.key() == QtCore.Qt.Key_F6:
            self.label.setText("?")

    def mousePressEvent(self, event):
        self.offset = event.pos()
        if self.BB_top_left and self.BB_top_right:
            # image = Image.open('5outof16.png')
            self.image = ImageGrab.grab(bbox=(self.BB_top_left[0],self.BB_top_left[1],self.BB_top_right[0],self.BB_top_right[1]))
            self.image = self.image.convert('L')
            self.image = PIL.ImageOps.invert(self.image)
            OCRImage = pytesseract.image_to_string(self.image)
            splitOCRImage = re.findall("(\d*)/(\d*)", OCRImage)
            # print(splitOCRImage)
            if len(splitOCRImage) != 1 or len(splitOCRImage[0]) != 2:
                self.label.setText("?")
            else:
                # print(self.BB_top_left, self.BB_top_right, OCRImage, splitOCRImage)
                # print(splitOCRImage)
                self.label.setText(str(ceil(((int(splitOCRImage[0][1]) - int(splitOCRImage[0][0])) / 4)) * 5))
        
    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        xw = self.offset.x()
        yw = self.offset.y()
        self.move(x-xw, y-yw)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.setTopLevelWindow()
            self.dialog.close()

            return True

        return False


pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

print("=================")
print("OVERLAY DISPLAYED")
print("=================")

app = QtWidgets.QApplication(sys.argv)
mywindow = mymainwindow()
mywindow.show()
app.exec_()
