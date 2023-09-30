from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QPushButton, QLabel, QListWidget, QFileDialog,
        QLineEdit, QTextEdit, QInputDialog,
        QHBoxLayout, QVBoxLayout
               )
import os
from PIL import Image
from PyQt5.QtGui import QPixmap

app = QApplication([])
MainWindow = QWidget()

MainWindow.setWindowTitle('Картинки...')
MainWindow.resize(900, 700)

btn_dir = QPushButton('Папка')
list_filles = QListWidget()
image = QLabel('Картинка')
btn_left = QPushButton('Влево')
btn_right = QPushButton('Вправо')
btn_mirror = QPushButton('Отзеркалить')
btn_contr = QPushButton('Контраст')
btn_BW = QPushButton('Ч/Б')

line1 = QVBoxLayout()
line1.addWidget(btn_dir)
line1.addWidget(list_filles)

line3 = QHBoxLayout()
line3.addWidget(btn_left)
line3.addWidget(btn_right)
line3.addWidget(btn_mirror)
line3.addWidget(btn_contr)
line3.addWidget(btn_BW)
line2 = QVBoxLayout()
line2.addWidget(image)
line2.addLayout(line3)

main_line = QHBoxLayout()
main_line.addLayout(line1, 30)
main_line.addLayout(line2, 80)
MainWindow.setLayout(main_line)

def Filterr(files, extensions):
    result_list = []
    for fail in files:
        for ex in extensions:
            if fail.endswith(ex):
                result_list.append(fail)
    return result_list
    
workdir = ''
def WorkDir():
    global workdir 
    workdir = QFileDialog.getExistingDirectory()

def ShowFiles():
    ext = ['png', 'jpg', 'jpeg', 'svg']
    WorkDir()
    filenames = Filterr(os.listdir(workdir), ext)
    list_filles.clear()
    for file in filenames:
        list_filles.addItem(file)
btn_dir.clicked.connect(ShowFiles)

class ImageProc():
    def __init__(self):
        self.image = None
        self.name = None
        self.dir = None
        self.save_dir = 'change'

    def loadImage(self, filename):
        self.name = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
    def showImage(self, path):
        image.hide()
        pixmapimage = QPixmap(path)
        w,h = image.width(), image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmapimage)
        image.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.name)
        self.image.save(image_path)
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.name)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.name)
        self.showImage(image_path)
    
    def left(self):
        self.image = self.image.transpose(image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.name)
        self.showImage(image_path)

    def right(self):
        self.image = self.image.transpose(image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.name)
        self.showImage(image_path)

    def contrast(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.name)
        self.showImage(image_path)



workimage = ImageProc()
    
def showChosenImage():
        if list_filles.currentRow() >= 0:
            filename = list_filles.currentItem().text()
            workimage.loadImage(filename)
            image_path = os.path.join(workdir, workimage.name)
            workimage.showImage(image_path) 
list_filles.currentRowChanged.connect(showChosenImage)
btn_BW.clicked.connect(workimage.do_bw)  
btn_left.clicked.connect(workimage.left)
btn_right.clicked.connect(workimage.right)
btn_contr.clicked.connect(workimage.contrast)

btn_mirror.clicked.connect(workimage.do_flip) 
MainWindow.show()
app.exec_()
