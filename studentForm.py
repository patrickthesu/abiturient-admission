#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QScrollArea
import sys
import db

from components.inputs import nameInput, phoneEdit, adressEdit
from components.selectWidgets import schoolSelect, languageSelect

connect = db.Connection ()

class gradeTypes (QWidget):
    def __init__ (self):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.gradeTypes = []

        for gradeType in connect.getGradeTypes ():
            self.gradeTypes.append (QCheckBox (gradeType[1]))
            self.gradeTypes[len(self.gradeTypes)-1].stateChanged.connect ( self.check )
            self.layout.addWidget ( self.gradeTypes[len(self.gradeTypes)-1] )

        self.errorLabel = QLabel ("Необходимо выбрать хотя-бы один профиль")
        self.layout.addWidget ( self.errorLabel )
        self.errorLabel.setStyleSheet ( "color: red;" )
        self.errorLabel.hide()

    def check (self):
        self.errorLabel.hide()
        for gradeType in self.gradeTypes:
            if gradeType.isChecked(): return True
        return self.error()

    def error (self):
        self.errorLabel.show ()
        return False
    
    def __call__ (self):
        if not self.check (): return False
        out = [] 
        for i in range ( len ( self.gradeTypes)):
            if self.gradeTypes[i].isChecked(): out.append ( i+1 )
        return out

class studentFinalData (QWidget):
    def __init__ (self, selectedGradesIds = [], name = "Вы не ввели имя, обратитесь в администрацию", ID = "Ошибка регистрации" ):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.setWindowTitle ( "Успешно!" )

        self.layout.addWidget ( QLabel ( name + ",\nпоздравляем, вы были успешно зарегистрированы" ) )
        self.layout.addWidget ( QLabel ( "Запомните ваш уникальный номер:" ) )
        self.layout.addWidget ( QLabel ( str(ID) ) )

        self.examList = examList ( selectedGradesIds )
        self.layout.addWidget ( self.examList )


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

 
class studentForm (QWidget):
    def __init__ (self):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        self.setWindowTitle ( "Заполнение форму" )

        self.layout.addWidget ( QLabel ( "Введите ваше имя:" ))
        self.nameInput = nameInput ()
        self.layout.addWidget ( self.nameInput )

        self.layout.addWidget ( QLabel ( "Ваш номер телефона:" ))
        self.phoneEdit = phoneEdit ()
        self.layout.addWidget ( self.phoneEdit )

        self.layout.addWidget ( QLabel ( "Ваш адрес:" ))
        self.adressEdit = adressEdit ()
        self.layout.addWidget ( self.adressEdit )

        self.layout.addWidget ( QLabel ( "Выберете профиль:" ))
        self.gradeTypes = gradeTypes()
        self.layout.addWidget ( self.gradeTypes )

        self.layout.addWidget ( QLabel ( "Ваш город:" ))
        self.schoolSelect = schoolSelect (connect)
        self.layout.addWidget (self.schoolSelect)

        self.layout.addWidget ( QLabel ( "Языки которые вы знаете:" ))
        self.languageSelect = languageSelect (connect)
        self.layout.addWidget ( self.languageSelect )
        self.submitButton = QPushButton ( "Зарегистрироваться " )
        self.submitButton.clicked.connect ( self.submit )
        self.layout.addWidget ( self.submitButton )

    def submit (self):
        name = self.nameInput()
        if not name:
            print ( "ERROR incorrect fullname" )
            return False
        grades = self.gradeTypes ()
        if not grades:
            print ( "ERROR not selected grades" )
            return False  
        schoolId = self.schoolSelect()
        if not schoolId: 
            print ( "ERROR SCHOOL ID" )
            return False
        phone = self.phoneEdit()
        if not phone: 
            print ( "ERROR PHONE ID" )
            return False
        adress = self.adressEdit()
        if not adress: 
            print ( "ERROR INVALID ADRESS" )
            return False
        languages = self.languageSelect ()
        if not languages:
            print ( "ERROR Languages ids" )
            return False
        lastId = connect.insertStudent ( name, schoolId["school_id"], phone, adress)[0]
        connect.insertLanguageSet ( lastId, languages["primary_id"], languages["foreign_id"])
        connect.insertGradeSets ( lastId, grades)
        self.examList = studentFinalData ( grades, name, lastId )
        self.examList.show ()
        self.close ()

if __name__ == "__main__":
    app = QApplication ( sys.argv )
    mv = studentForm ()
    mv.show()
    app.exec ()
