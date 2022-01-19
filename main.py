import os, sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
    QSizePolicy, QLabel, QFontDialog, QApplication, QFileDialog)
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import functions as fc
from tensorflow.keras.models import load_model
import GUI2
import dialog
from learning import learning
#from dialog import Ui_Dialog as dialog

class Label:
    def f(self1, self):
        print(self.name.text())
        #print('adsfhjkl')

    def open(nisemono, self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(caption = "Выберите папку с классифицированными документами")
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            #for file_name in os.listdir(directory):  # для каждого файла в директории
            self.path.setText(directory)   # добавить файл в listWidget


    def __init__(self, path, name, check, btn):
        self.check = check
        self.path = path
        self.name = name
        self.btn = btn
        #print('awrewrewrewrewrwerewrwersdf')

        self.btn.clicked.connect(lambda: self.open(self))
        
            

class ExampleAppDialog(QtWidgets.QDialog, dialog.Ui_Dialog): ######DIALOG######
    
    def __init__(self):
            
        super().__init__()
        self.setupUi(self)
        self.Undo.clicked.connect(self.close)
        self.Start.clicked.connect(self.learning_)

        self.labeles_list = []

        self.labeles_list.append(Label(self.lineEdit_4, self.lineEdit_6,  self.checkBox,   self.pushButton)) 
        self.labeles_list.append(Label(self.lineEdit_3,   self.lineEdit_7,  self.checkBox_2, self.pushButton_2))
        self.labeles_list.append(Label(self.lineEdit, self.lineEdit_8,  self.checkBox_3, self.pushButton_3))
        self.labeles_list.append(Label(self.lineEdit_2, self.lineEdit_9, self.checkBox_4, self.pushButton_4))
        self.labeles_list.append(Label(self.lineEdit_5, self.lineEdit_10, self.checkBox_5, self.pushButton_5))

    
    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку с классифицированными документами")
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.lineEdit.setText(directory)   # добавить файл в listWidget

    def learning_(self):
        paths = []
        classnames = []
        
        modelname = self.ClassName_line.text()

        for i in range(5):
            if self.labeles_list[i].check.isChecked():
                path = self.labeles_list[i].path.text()
                if not os.path.isdir(path):
                    self.textEdit.append(f'Укажите правильный путь (неправильный путь {i + 1})')
                    return
                paths.append(self.labeles_list[i].path.text())
                classnames.append(self.labeles_list[i].name.text())

        if not (len(paths) == 0):
            print(paths, '\n\n', classnames, '\n\n', modelname)
            try:
                learning(paths, classnames, modelname)
            except Exception as e:
                self.textEdit.append('Укажите правильный путь')
                print(e)
        else:
            self.textEdit.append('Пути к файлам указаны неверно или не указаны')
        
    

    

class ExampleApp(QtWidgets.QMainWindow, GUI2.Ui_MainWindow): #####MAIN#####
    
    

    def browse_folder(self):
        self.lineEdit.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку с неклассифицированными документами")
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
            
            self.lineEdit.setText(directory)   # добавить файл в listWidget

    def browse_model(self):
        self.lineEdit_2.clear()
        directory = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл модели")
        print("##########################################3", directory[0])
        if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
           
            self.lineEdit_2.setText(directory[0])   # добавить файл в listWidget
   
   
    def use(self, modelname):
    
        if not (os.path.isdir(self.lineEdit.text()) and os.path.isfile(self.lineEdit_2.text())):
            self.textEdit.append('Путь к документам и/или файлу модели указан неверно')
            return

        try:
            model=load_model(self.lineEdit_2.text())
            pred = fc.usenet(self.lineEdit.text(), model)

            fc.rename(self.lineEdit.text(), self.lineEdit_2.text(), pred)
        except OSError:
            self.textEdit.append('Укажи')

    

    
    def __init__(self):       
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.browse_folder)
        self.pushButton_2.clicked.connect(self.use)
        self.dial = ExampleAppDialog()
        self.Learning.clicked.connect(self.dial.exec)###############################################################################
        self.ClassButton.clicked.connect(self.browse_model)
    


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    main_window = ExampleApp()  # Создаём объект класса ExampleApp
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    main_window.show()  # Показываем окно
    dial = ExampleAppDialog()
    app.exec_()  # и запускаем приложение
      
    

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()