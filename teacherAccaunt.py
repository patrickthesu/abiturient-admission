#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox, QComboBox
from PyQt6.QtCore import pyqtSlot
from kvqtlib.table import tableWidget
import sys
import db

connect = db.Connection ()

class passwordInput (QWidget):
    def __init__ (self):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.edit = QLineEdit ()
        self.edit.setEchoMode(QLineEdit.EchoMode.Password)
 
        self.layout.addWidget (self.edit)

    def __call__ (self):
        return self.edit.text()

class nameInput (QWidget):
    def __init__ (self):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.edit = QLineEdit ()
        self.layout.addWidget (self.edit)
        self.edit.editingFinished.connect ( self.check )

        self.errorLabel = QLabel ( "ФИО некорректное" )
        self.errorLabel.setStyleSheet ( "color: red;" )

        self.layout.addWidget ( self.errorLabel )
        self.errorLabel.hide ()

    def check (self):
        self.errorLabel.hide ()
        name = self.edit.text().strip().split()
        if len ( name ) < 2: return self.error ( "Неправильное полное имя" )
        return True
        
    def error (self, text):
        self.errorLabel.setText (text)
        self.errorLabel.show ()
        return False

    def __call__ (self):
        if not self.check():
            return False
        return self.edit.text()



class teacherLogin ( QWidget):
    def __init__ (self, function = lambda: print("Not setted function") ):
        super (QWidget, self).__init__ ()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.function = function

        self.layout.addWidget (QLabel ("Вход в личный кабинет"))

        self.errorLabel = QLabel ( "Такого пользователя нет в базе" )
        self.errorLabel.setStyleSheet ( "color: yellow;" )
        self.layout.addWidget ( self.errorLabel )
        self.errorLabel.hide ()

        self.layout.addWidget (QLabel ("Введите ваше ФИО:"))
        self.nameInput = nameInput ()
        self.layout.addWidget (self.nameInput)
        self.layout.addWidget (QLabel ("Введите ваш пароль:"))
        self.passwordInput = passwordInput ()
        self.layout.addWidget ( self.passwordInput )
        self.loginButton = QPushButton ( "Войти" )
        self.loginButton.clicked.connect ( self.login )
        self.layout.addWidget (self.loginButton)

    def login (self):
        self.errorLabel.hide ()
        name = self.nameInput ()
        if not name:
            print ( "ERROR incorrect name" )
            return False
        password = self.passwordInput ()
        if not password:
            print ( "ERROR incorrect name" )
            return False

        try:
            teacher = connect.getTeacher ( name )
            #print ( teacher )
            if password == teacher[0][2]: 
                #print ( f"Teacher '{teacher}' logined" )
                self.function ( teacher[0][0] )
            else:
                return self.errorLabel.show() 
        except:
            return self.errorLabel.show()
        self.close()



class insertCabinet ( QWidget ):
    def __init__ (self, function = lambda: print ("Succesfully added cabinet!")): 
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.function = function

        self.layout.addWidget ( QLabel ( "Введите название кабинета:" ))
        self.name = QLineEdit ()
        self.layout.addWidget (self.name)

        self.layout.addWidget ( QLabel ( "Кол-во парт в кабинете:" ))
        self.itemcount = QSpinBox ()
        self.itemcount.setMinimum (1)
        self.itemcount.setMaximum (100)
        self.layout.addWidget ( self.itemcount )
        
        self.layout.addWidget ( QLabel ( "Максимальное кол-во учеников за партой:" ))
        self.item = QSpinBox ()
        self.item.setMinimum (1)
        self.item.setMaximum (100)
        self.layout.addWidget ( self.item )

        self.submitButton = QPushButton ( "Добавить кабинет" )
        self.submitButton.clicked.connect ( self.submit )
        self.layout.addWidget ( self.submitButton )

    def check (self):
        if self.name.text().strip() == "":
            return False
        return True

    def submit (self):
        if not self.check ():
            return False
        try:
            connect.insertCabinet ( self.name.text(), self.itemcount.value(), self.item.value())
            self.function ()
            self.close()
        except Exception as err:
            print ("ERROR while pushing")
            print (err)

class showExamLists (QWidget):
    def __init__ (self):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.allExams = connect.getAllExamsNames ()
        self.examsCombo = QComboBox ()

        for exam in self.allExams:
            self.examsCombo.addItem ( exam[0], userData = exam[1] )

        examData = self.examsCombo.currentData ()
        studentsList = connect.getFullExam ( examData [0], examData[1] )  
        self.tableWidget = tableWidget ( headers = ["Имя", "Номер телефона", "Адресс", "Кабинет"], columns = studentsList, vertical = False)
        self.layout.addWidget (self.tableWidget)
 
        self.layout.addWidget ( self.examsCombo )
        self.examsCombo.currentIndexChanged.connect ( self.setTable )

    def setTable ( self ):
        examData = self.examsCombo.currentData ()
        studentsList = connect.getFullExam ( examData [0], examData[1] ) 
        self.tableWidget.setTable ( studentsList, vertical = False )


class makeExamList ( QWidget ):
    def __init__ ( self ):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.autoGenerateButton = QPushButton ( "Сгенерировать автоматически" )
        self.autoGenerateButton.clicked.connect ( self.autoGenerate )
        self.layout.addWidget ( self.autoGenerateButton )

    def autoGenerate (self):
        self.close ()
        connect.makeAutoAllExams ()
        self.examLists = showExamLists ()
        self.examLists.show ()

class cabinetsManage ( QWidget ):
    def __init__ ( self ):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.layout.addWidget ( QLabel ("Управление кабинетами") )
        self.setWindowTitle ("Управление кабинетами")

        self.cabinets = connect.getCabinets ()
        self.tableWidget = tableWidget ( headers = ["ID", "Название", "Кол-во парт", "Учеников на парту"], columns = self.cabinets, vertical = False)
        self.layout.addWidget (self.tableWidget)
        self.insertCabinetButton = QPushButton ( "Добавить кабинет" )
        self.insertCabinetButton.clicked.connect ( self.insertCabinet )
        self.layout.addWidget ( self.insertCabinetButton )

    def refresh (self):
        self.cabinets = connect.getCabinets ()
        self.tableWidget.setTable ( self.cabinets, False )

    def insertCabinet ( self ):
        self.insertCabinetWindow = insertCabinet ( function = lambda: self.refresh() )
        self.insertCabinetWindow.show()

class SetMark ( QWidget ):
    def __init__ (self, examId, profile, student, function = lambda: print ( "ERROR: invalid SetMark init" )):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.examId = examId
        self.profile = profile
        self.student = student
        self.function = function

        self.layout.addWidget ( QLabel ("Поставить оценку за екзамен для:") )
        self.layout.addWidget ( QLabel (str ( self.student[1] )) )

        self.markInput = QSpinBox ()
        self.markInput.setMinimum (0)
        self.markInput.setMaximum (100)
        self.layout.addWidget ( self.markInput )

        confirmButton = QPushButton ( "Подтвердить" )
        confirmButton.clicked.connect ( self.setMark )
        self.layout.addWidget (confirmButton)

    def setMark (self):
        try:
            connect.setMark ( self.markInput.value(), self.student[0], self.examId, self.profile )
            self.close ()
            self.function ()
        except Exception as err:
            print ( "ERROR: on setting mark" )
            print ( err )

class StudentsExamList ( QWidget ):
    def __init__ ( self, examList, examData, teacherId = None, endParent = lambda: print ( "ERROR: Invalid studentExamList init" ) ):
        super (QWidget, self).__init__()
        self.examList = examList
        self.examData = examData
        self.endParent = endParent

        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.layout.addWidget ( QLabel ( "Выберите ученика которуму собираетесь поставить оценку:" ))

        self.students =  []

        for student in self.examList:
            studentButton = QPushButton ( student[1] )
            studentButton.data = student
            studentButton.clicked.connect ( self.takeExam )
            self.students.append ( studentButton )
            self.layout.addWidget (studentButton)

    def isFinal (self):
        for studentButton in self.students:
           if not studentButton.isHidden() : 
                return False
        return True

    @pyqtSlot ()
    def takeExam (self):
        sender = self.sender()
        sender.hide ()
 
        # print ( sender.data )

        self.setMark = SetMark ( self.examData[0], self.examData[1], sender.data, lambda: self.endExam () if self.isFinal () else None )        
        self.setMark.show()

    def endExam (self):
        print ( "Ending..." )

        self.endWidget = QWidget ()

        layout = QVBoxLayout ()
        layout.addWidget ( QLabel( "Поздравляем вас!\nЕкзамен закончился" ) )
        closeButton = QPushButton ( "Oк" )
        closeButton.clicked.connect ( lambda: self.endWidget.close () )
        layout.addWidget ( closeButton )

        self.endWidget.setLayout ( layout )
        self.endWidget.setWindowTitle ( "Конец" )

        self.close ()
        self.endParent ()
        self.endWidget.show()


class ExamsList (QWidget):
    def __init__ ( self, teacherId = None, function = lambda examsList, examData: print ( "ERROR: invalid ExamsList init" )):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.function = function

        self.layout.addWidget ( QLabel ("Выберите екзамен который вы хотите провести:") )

        allExams = connect.getAllExamsNames ()
        for exam in allExams:
            examData = exam[1]
            examList = connect.getFullExam ( examData [0], examData[1] )
            if len (examList) == 0: continue

            button = QPushButton ( exam[0] )
            button.data = exam[1]
            button.clicked.connect (self.selectExam)

            self.layout.addWidget ( button )

    @pyqtSlot ()
    def selectExam (self):
        examData =  self.sender().data
        examsList = connect.getFullExam ( examData [0], examData[1], True )
        self.function ( examsList, examData )
               

class Exam ( QWidget ):
    def __init__ (self, teacherId = None):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.teacherId = teacherId

        self.examsList = ExamsList ( teacherId, self.selectExam )
        self.layout.addWidget (self.examsList)

    def selectExam ( self, examList, examData ):
        self.examsList.hide()
        self.studentExamsList = StudentsExamList ( examList, examData, self.teacherId, self.close )
        self.layout.addWidget (self.studentExamsList)

class mainMenu ( QWidget ):
    def __init__ (self, teacher_id):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.teacher = connect.getTeacher ( teacher_id = teacher_id )
        self.layout.addWidget ( QLabel ( str ( self.teacher[0][1]) ) )
        self.setWindowTitle ("Меню учителя")
        self.layout.addWidget ( QLabel ("Меню учителя:") )
        self.cabinetsButton = QPushButton ( "Управление кабинетами" )
        self.cabinetsButton.clicked.connect ( self.cabinetsManage )
        self.layout.addWidget ( self.cabinetsButton )
        self.makeExamButton = QPushButton ( "Провести экзамен" )
        self.layout.addWidget (self.makeExamButton )
        self.makeExamButton.clicked.connect ( self.makeExam )
        self.formListsButton = QPushButton ( "Сформировать екзамены" )
        self.formListsButton.clicked.connect ( self.makeExamLists )
        self.layout.addWidget ( self.formListsButton )
        self.checkResultsButton = QPushButton ( "Просмотреть результаты" )
        self.layout.addWidget (self.checkResultsButton )

    def makeExamLists ( self ):
        self.examListsWindow = makeExamList ()
        self.examListsWindow.show ()

    def cabinetsManage ( self ):
        self.cabinetsManageWindow = cabinetsManage ()
        self.cabinetsManageWindow.show()

    def makeExam ( self ):
        self.exam = Exam ()
        self.exam.show()

class main ():
    def __init__ (self):
        self.app = QApplication ( sys.argv )
        self.login = teacherLogin ( lambda teacher_id: self.logined (teacher_id) )
        self.login.show()
        self.app.exec()
    def logined (self, teacher_id):
        try:
            self.mw = mainMenu(teacher_id)
            self.mw.show()
        except Exception as err:
            print (err)

if __name__ == "__main__":
    app = main ()
