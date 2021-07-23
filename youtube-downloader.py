from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.uic import loadUiType
import os
from os import path
from os.path import expanduser
import sys
import pafy
import math
import urllib.request


#import UI File
FORM_CLASS ,_ = loadUiType(path.join(path.dirname(__file__),"main.ui"))


#Initiate UI File
class MainApp(QMainWindow, FORM_CLASS):

    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_UI()
        self.handle_Buttons()
        self.handle_Actions()
        self.setWindowIcon(QIcon('icons/youtube.png'))

    def handle_UI(self):
        self.setFixedSize(741,548)

    def handle_Buttons(self):
        self.pushButton.clicked.connect(self.handle_Browse)
        self.pushButton_2.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_3.clicked.connect(self.Get_Video_Info)


    def handle_Actions(self):
        self.actionExit.triggered.connect(self.action_exit)
        self.actionAbout.triggered.connect(self.action_about)


    def action_exit(self):
        QApplication.exit()


    def action_about(self):
        msg = '''
       
YouTube Downloader v1.0

==========================
Author: irison
GitHub: https://github.com/0xirison
*._.* __ _ ._ 
|[  |_) (_)[ )
==========================        
                           
This tool is built by Python 3.6, it is used for downloading YouTube videos

Enjoy!

        '''
        QMessageBox.information(self, "About the Application", msg)


    def handle_Browse(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Download Directory", expanduser("~/Desktop"))
        self.lineEdit_2.setText(dir_path)


    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return '{} {}'.format(s , size_name[i])

    def Get_Video_Info(self):
        self.comboBox.clear()
        url_link = self.lineEdit.text()
        try:
            video = pafy.new(url_link)
        except:
            QMessageBox.warning(self, "URL is invalid", "Please insert a valid YouTube video link")
            self.lineEdit.setText('')
            return

        st = video.videostreams
        if str(st).find("mp4") < 0:
            for i in st:
                data = '{} {} {}'.format(i.resolution, i.extension, self.convert_size(i.get_filesize()))
                self.comboBox.addItem(data)
        else:
            for video in st:
                if video.extension == "mp4":
                    vide_reso = video.resolution.split("x")[1] + "p"
                    data = '{} - {} - {}'.format(vide_reso, video.extension.upper(), self.convert_size(video.get_filesize()))
                    self.comboBox.addItem(data)
        count = self.comboBox.count()-1
        self.comboBox.setCurrentIndex(count)
        QApplication.processEvents()
        link = self.lineEdit.text()
        yt = pafy.new(link)
        url_image = yt.thumb
        image = QImage()
        image.loadFromData(urllib.request.urlopen(url_image).read())
        self.label_2.setScaledContents(1)
        self.label_2.setPixmap(QPixmap(image))
        self.label.setText(yt.title)


    def change_Filename(self, file_dir, filename, extension= '.mp4'):
        os.chdir(file_dir)
        counter = 1
        original_name = filename + '' + extension
        file_fullname = original_name
        while os.path.isfile(file_fullname):
            file_fullname = str(filename + '({})'.format(counter)) + extension
            counter += 1
        os.rename(original_name+".temp", file_fullname)


    def Download_Youtube_Video(self):
        if not os.path.isdir(self.lineEdit_2.text()):
            QMessageBox.warning(self, "Directory Path is Invalid", "Please select a valid directory path")
            self.lineEdit_2.setText('')
            return

        video_link = self.lineEdit.text()
        dir_path = self.lineEdit_2.text()
        try:
            video = pafy.new(video_link)
        except:
            QMessageBox.warning(self, "URL is invalid", "Please insert a valid YouTube video link")
            self.lineEdit.setText('')
            return

        st = video.videostreams
        quality = self.comboBox.currentIndex()
        ext = str(self.comboBox.currentText()).lower()
        extension = ""
        media_list = ['ogg', 'm4a', 'mp4', 'flv', 'webm', '3gp']
        for media_type in media_list:
            if ext.find(media_type) >= 0:
                extension = media_type

        try:
            st[quality].download(filepath=dir_path, callback=self.handle_Progressbar)
        except FileExistsError:
            extension = '.' + extension
            self.change_Filename(dir_path,video.title, extension)
            QApplication.processEvents()
        except Exception as e:
            QMessageBox.critical(self, "Download Failed", "Something went wrong, please try again..")
            print(e)
        self.cleanUp()


    def cleanUp(self):
        self.label.setText('Youtube Video Title')
        self.comboBox.clear()
        self.label_2.clear()
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)
        self.lineEdit.setText('')


    def handle_Progressbar(self, total, recvd, ratio, rate, eta):
        self.progressBar.setValue(ratio * 100)
        if ratio * 100 == 100.00:
            QMessageBox.information(self, "File Status", "Download Finished")
            self.progressBar.setValue(0)
        QApplication.processEvents()


def main():
        app = QApplication(sys.argv)
        window = MainApp()
        window.show()
        app.exec()


if __name__ == "__main__":
    main()