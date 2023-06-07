#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from kvqtlib.table import tableWidget
from kvqtlib.errors import errorWindow
import sys
import db

from components.inputs import passwordInput, nameInput, idInput

global DB_ERROR
try:
    connect = db.Connection ()
    DB_ERROR = False
except:
    DB_ERROR = True

class examList (QWidget):
    def __init__ (self, selectedGradesIds = [], studentId = None ):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        if len ( selectedGradesIds ) == 0:
            try:
                grades = connect.getGradesByStudent ( studentId )
                for i in range ( grades ):
                    selectedGradesIds.append ( grades [i][0] )
            except:
                self.layout.addWidget ( QLabel ( "Похоже вы не выбрали профиль (" ))
                self.layout.addWidget ( QLabel ( "Попробуйте ещё раз зарегистрироваться" ))
                return
        
        
        self.layout.addWidget ( QLabel ( "Ваш список екзаменов:" ) )
        for exam in connect.getExams (selectedGradesIds):
            self.layout.addWidget ( QLabel ( exam ) )


class studentAccount (QWidget):
    def __init__ ( self, studentId, studentName = "Ошибка! Сообщите администрации!" ):
        super (QWidget, self).__init__ ()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)
        self.setWindowTitle ("Личный кабинет")

        self.layout.addWidget ( QLabel ( "Добро пожаловать, " + studentName ) )

        exams = connect.getExamsCabinetsList ( studentId )
        if len ( exams ) == 0:
            self.layout.addWidget (QLabel ("Похоже вас ещё не распределили =("))
            self.examList = examList (studentId = studentId )
            self.layout.addWidget ( self.examList )
            print ( "No exams" )
            return 
 
        self.layout.addWidget ( QLabel ("Ваш список экаменов"))
        self.table = tableWidget ( ["Екзамен", "Профильный", "Кабинет", "Дата", "Оценка"], exams, vertical = False )
        self.layout.addWidget ( self.table )



class studentLogin ( QWidget ):
    def __init__ (self):
        super (QWidget, self).__init__ ()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.layout.addWidget (QLabel ("Вход в личный кабинет"))

        self.errorLabel = QLabel ( "Такого пользователя нет в базе" )
        self.errorLabel.setStyleSheet ( "color: yellow;" )
        self.layout.addWidget ( self.errorLabel )
        self.errorLabel.hide ()

        self.layout.addWidget (QLabel ("Введите ваше ФИО:"))
        self.nameInput = nameInput ()
        self.layout.addWidget (self.nameInput)
        self.layout.addWidget (QLabel ("Введите ваш уникальный номер:"))
        self.idInput = idInput ()
        self.layout.addWidget ( self.idInput )
        self.signinButton = QPushButton ( "Зарегистрироваться" )
        self.signinButton.clicked.connect ( self.signin )
        self.signinButton.setStyleSheet ( """color: rgb(98, 240, 215); padding-bottom: 10px; border: None;""" )
        self.layout.addWidget (self.signinButton)
        self.loginButton = QPushButton ( "Войти" )
        self.loginButton.clicked.connect ( self.login )
        self.layout.addWidget (self.loginButton)

    def signin (self):
        self.close ()
        from studentForm import studentForm
        self.sf = studentForm ()
        self.sf.show ()
        

    def login (self):
        self.errorLabel.hide ()
        name = self.nameInput ()
        if not name:
            print ( "ERROR incorrect name" )
            return False
        sid = self.idInput ()
        if not sid:
            print ( "ERROR incorrect name" )
            return False

        try:
            if name == connect.getStudentName ( sid )[0][0]: 
                self.close ()
                self.studentAccount = studentAccount ( sid, name )
                self.studentAccount.show ()
            else:
                return self.errorLabel.show() 
        except Exception as err:
            print ( err )
            return self.errorLabel.show()

if __name__ == "__main__":
    app = QApplication ( sys.argv )
    if DB_ERROR:
        self.errorWindow = errorWindow ()
        self.errorWindow.errorTemplate ("Ошибка при подключении к базе данных.\nУведомите об этом администратора.") 
    else:
        mv = studentLogin ()
        mv.show()
    app.exec ()
