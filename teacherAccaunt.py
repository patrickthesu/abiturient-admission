#!/usr/bin/env python3

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox, QDoubleSpinBox, QComboBox, QCheckBox, QDateEdit 
from PyQt6.QtCore import pyqtSlot, QDate
from kvqtlib.table import tableWidget
from kvqtlib.errors import errorWindow
from kvqtlib.files import writeWidget
from datetime import datetime
from components.inputs import nameInput, passwordInput
import pandas as pd
import sys
import db


global DB_ERROR
try:
    connect = db.Connection ()
    DB_ERROR = False
except:
    DB_ERROR = True


class teacherLogin ( QWidget):
    def __init__ (self, function = lambda: print("Not setted function") ):
        super (QWidget, self).__init__ ()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)

        self.function = function 
        self.layout.addWidget (QLabel ("Вход в личный кабинет"))
        self.resize(500,200)

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
            if password == teacher[0][2]: 
                self.function ( teacher[0][0] )
            else: return self.errorLabel.show() 
        except:
            return self.errorLabel.show()
        self.close()


class insertExamGradetype (QWidget):
    def __init__ (self, function = lambda: print ("Succesfully added insertExamGradetype!")): 
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.function = function

        self.layout.addWidget ( QLabel ("Введите индекс экзамена:"))
        self.exam = QSpinBox ()
        self.exam = QSpinBox ()
        self.exam.setMinimum (1) 
        self.layout.addWidget (self.exam)

        self.layout.addWidget ( QLabel ("Введите индекс профиля обучения:"))
        self.gradetype = QSpinBox () 
        self.gradetype.setMinimum (1)
        self.layout.addWidget ( self.gradetype )

        self.profile = QCheckBox ("Профильный")
        self.layout.addWidget (self.profile)

        self.submitButton = QPushButton ( "Добавить связку" )
        self.submitButton.clicked.connect ( self.submit )
        self.layout.addWidget ( self.submitButton )

    def submit (self):
        try:
            connect.insertExamGradetype (self.exam.value (), self.gradetype.value (), self.profile.isChecked())
            self.function ()
            self.close()
        except Exception as err:
            print ("ERROR while pushing gradetype")
            print (err)

class deleteExamGradetype (QWidget):
    def __init__ (self, function = lambda: print ("Succesfully deleted!")): 
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.function = function

        self.layout.addWidget ( QLabel ("Введите индекс экзамена:"))
        self.exam = QSpinBox ()
        self.exam = QSpinBox ()
        self.exam.setMinimum (1) 
        self.layout.addWidget (self.exam)

        self.layout.addWidget ( QLabel ("Введите индекс профиля обучения:"))
        self.gradetype = QSpinBox ()
        self.gradetype.setMinimum (1)
        self.layout.addWidget ( self.gradetype )

        self.submitButton = QPushButton ( "Удалить экзамен" )
        self.submitButton.clicked.connect ( self.submit )
        self.layout.addWidget ( self.submitButton )

    def submit (self):
        try:
            connect.deleteExamGradetype (self.exam.value (), self.gradetype.value ())
            self.function ()
            self.close()
        except Exception as err:
            self.errorWindow = errorWindow ()
            self.errorWindow.errorTemplate ("Ошибка при удалении, убедись что такой индекс существует в таблице.")
            self.errorWindow.show ()
            print ("ERROR while deleting gradetype")
            print (err)


class deleteCabinet (QWidget):
    def __init__ (self, function = lambda: print ("Succesfully deleted!")): 
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.function = function

        self.layout.addWidget ( QLabel ("Введите индекс каибинета:"))
        self.cabinet = QSpinBox ()
        self.cabinet.setMinimum (1) 
        self.layout.addWidget (self.cabinet)

        self.submitButton = QPushButton ( "Удалить кабинет" )
        self.submitButton.clicked.connect ( self.submit )
        self.layout.addWidget ( self.submitButton )

    def submit (self):
        try:
            connect.deleteCabinet (self.cabinet.value ())
            self.function ()
            self.close()
        except Exception as err:
            print ("ERROR while deleting gradetype")
            print (err)

class makeGroups (QWidget):
    def __init__ (self):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.allGroups = connect.getGradeTypes ()
        self.groupCombo = QComboBox ()

        for exam in self.allGroups:
            self.groupCombo.addItem ( exam[1], userData = exam[0] )
 
        self.tableWidget = tableWidget ()
        self.layout.addWidget (self.tableWidget)

        self.setTable ()
 
        self.layout.addWidget ( self.groupCombo )
        self.groupCombo.currentIndexChanged.connect ( self.setTable )

        self.bottomLayout = QHBoxLayout ()

        self.bottomWidget = QWidget ()
        self.bottomWidget.setLayout (self.bottomLayout)
        self.layout.addWidget (self.bottomWidget)

        self.exportButton = QPushButton ("Экспортировать в таблицу")
        self.exportButton.clicked.connect (self.exportTable)
        self.bottomLayout.addWidget (self.exportButton)

        self.updateButton = QPushButton ("Обновить страницу")
        self.updateButton.clicked.connect (self.setTable)
        self.bottomLayout.addWidget (self.updateButton)

        self.getStudetnForSuccessButton = QPushButton ("Рекомендовать/Не рекомендовать к поступлению")
        self.getStudetnForSuccessButton.clicked.connect (self.getStudetnForSuccess)
        self.layout.addWidget (self.getStudetnForSuccessButton)

    def getStudetnForSuccess (self):
        groupData = self.groupCombo.currentData ()
        self.studentSuccess = StudentsSuccesSelecting (groupData)
        self.studentSuccess.show ()

    def setTable ( self ):
        groupData = self.groupCombo.currentData ()

        exams = connect.getExamsByGrade (groupData)

        headers = ["Имя", "Номер телефона", ]
        headers.append ("Зачислен(а)")
        for exam in exams:
            headers.append (exam) 
        headers.append ("Средняя оценка")

        studentsList = connect.getFullGrade ( groupData )  
        
        self.tableWidget.setTable (columns = studentsList, vertical = False)
        self.tableWidget.setHeaders (headers)


        #self.data = {'Имя': [],'Номер':[],'Кабинет': [],'Средняя оценка': []}
        #for student in studentList:
            #self.data['Имя'].append (student[0])
            #self.data['Номер'].append(student[1])
            #self.data['Средняя оценка'].append(student[2])

    #def setStudentsStatus (self):


    def exportTable (self):
        self.writeWidget = writeWidget (writeFunction = self.writeFile)
        self.writeWidget.show()

    def writeFile (self, filename):
        df = pd.DataFrame(self.data)
        df.to_excel (filename + ".xlsx")

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

        self.data = {'Имя': [],'Номер':[],'Кабинет': [],'Оценка': []}
        for student in studentsList:
            self.data['Имя'].append (student[0])
            self.data['Номер'].append(student[1])
            self.data['Оценка'].append(student[2])

        self.tableWidget = tableWidget ( headers = ["Имя", "Номер телефона", "Кабинет", "Оценка"], columns = studentsList, vertical = False)
        self.layout.addWidget (self.tableWidget)
 
        self.layout.addWidget ( self.examsCombo )
        self.examsCombo.currentIndexChanged.connect ( self.setTable )

        self.exportButton = QPushButton ("Экспортировать в таблицу")
        self.exportButton.clicked.connect (self.exportTable)

        self.bottomLayout = QHBoxLayout ()

        self.bottomWidget = QWidget ()
        self.bottomWidget.setLayout (self.bottomLayout)
        self.layout.addWidget (self.bottomWidget)

        self.exportButton = QPushButton ("Экспортировать в таблицу")
        self.exportButton.clicked.connect (self.exportTable)
        self.bottomLayout.addWidget (self.exportButton)

        self.updateButton = QPushButton ("Обновить страницу")
        self.updateButton.clicked.connect (self.setTable)
        self.bottomLayout.addWidget (self.updateButton)



    def setTable ( self ):
        examData = self.examsCombo.currentData ()
        studentsList = connect.getFullExam ( examData [0], examData[1] )
        self.tableWidget.setTable ( studentsList, vertical = False )
        self.data = {'Имя': [],'Номер':[],'Кабинет': [],'Оценка': []}
        for student in studentsList:
            self.data['Имя'].append (student[0])
            self.data['Номер'].append(student[1])
            self.data['Оценка'].append(student[2])

    def exportTable (self):
        self.writeWidget = writeWidget (writeFunction = self.writeFile)
        self.writeWidget.show()

    def writeFile (self, filename):
        df = pd.DataFrame(self.data)
        df.to_excel (filename + ".xlsx")


class makeExamList ( QWidget ):
    def __init__ ( self ):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.layout.addWidget (QLabel ("Введите дату проведения:"))
        
        now = datetime.now()

        self.date = QDateEdit(self)
        self.date.setDate(QDate(now.year, now.month, now.day))
        self.layout.addWidget (self.date)
        
        self.autoGenerateButton = QPushButton ( "Сгенерировать автоматически" )
        self.autoGenerateButton.clicked.connect ( self.autoGenerate )
        self.layout.addWidget ( self.autoGenerateButton )

    def autoGenerate (self):
        self.close ()
        connect.makeAutoAllExams (self.date.date().toString("yyyy.MM.dd"))
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
        self.deleteCabinetButton = QPushButton ( "Удалить кабинет" )
        self.deleteCabinetButton.clicked.connect ( self.deleteCabinet )
        self.layout.addWidget ( self.deleteCabinetButton )

    def refresh (self):
        self.cabinets = connect.getCabinets ()
        self.tableWidget.setTable ( self.cabinets, False )

    def insertCabinet (self):
        self.insertCabinetWindow = insertCabinet ( function = lambda: self.refresh() )
        self.insertCabinetWindow.show()

    def deleteCabinet (self):
        self.deleteCabinetWindow = deleteCabinet ( function = lambda: self.refresh() )
        self.deleteCabinetWindow.show()

class SetMarkWidget ( QWidget ):
    def __init__ (self, examId, profile, student, function = lambda: print ( "ERROR: invalid SetMarkWidget init" )):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)
        self.examId = examId
        self.profile = profile
        self.student = student
        self.function = function

        self.layout.addWidget ( QLabel ("Поставить оценку за екзамен для:") )
        self.layout.addWidget ( QLabel (str ( self.student["student_name"] )) )

        self.markInput = QSpinBox ()
        self.markInput.setMinimum (0)
        self.markInput.setMaximum (100)
        self.layout.addWidget ( self.markInput )

        confirmButton = QPushButton ( "Подтвердить" )
        confirmButton.clicked.connect ( self.setMark )
        self.layout.addWidget (confirmButton)

    def setMark (self):
        try:
            connect.setMark ( self.markInput.value(), self.student["student_id"], self.examId, self.profile )
            self.close ()
            self.function ()
        except Exception as err:
            print ( "ERROR: on setting mark" )
            print ( err )

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


class StudentsSuccesSelecting ( QWidget ):
    def __init__ ( self, gradetype_id: int ):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout ) 

        self.layout.addWidget (QLabel ("Выберите ученика, которого хотели оценить."))
        
        self.gradetype_id = gradetype_id

        self.studentsList = connect.getStudentsByGradetype (self.gradetype_id)
        self.students = []

        for student in self.studentsList:
            studentButton = QPushButton ( student[0] )
            studentButton.data = student
            studentButton.clicked.connect ( self.setSuccess )
            self.students.append (studentButton)
            self.layout.addWidget (studentButton)

    def isFinal (self):
        for studentButton in self.students:
           if not studentButton.isHidden() : 
                return False
        return True

    @pyqtSlot ()
    def setSuccess (self):
        sender = self.sender()
        sender.hide ()
 
        self.setMark = SetSuccessWidget ( sender.data, self.gradetype_id, lambda: self.endExam () if self.isFinal () else None )
        self.setMark.show()

    def endExam (self):
        print ( "Ending..." )

        self.endWidget = QWidget ()

        layout = QVBoxLayout ()
        layout.addWidget ( QLabel( "Поздравляем вас!\nВы оценили всех учеников." ) )
        closeButton = QPushButton ( "Oк" )
        closeButton.clicked.connect ( lambda: self.endWidget.close () )
        layout.addWidget ( closeButton )

        self.endWidget.setLayout (layout)
        self.endWidget.setWindowTitle ("Конец")

        self.close ()
        self.endWidget.show()

class SetSuccessWidget ( QWidget ):
    def __init__ (self, student, gradetype_id, function = lambda: print ( "ERROR: invalid SetMarkWidget init" )):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout (self.layout)
        self.student = student
        self.gradetype_id = gradetype_id
        self.function = function

        self.layout.addWidget ( QLabel ("Выберите рекомендацию к зачислению студента:") )
        self.layout.addWidget ( QLabel (str( self.student[0] )) )

        self.setSuccessButton = QPushButton ("Рекомендован к зачислению")
        self.layout.addWidget (self.setSuccessButton )
        self.setSuccessButton.clicked.connect (self.successStudent)
        self.setUnsuccessButton = QPushButton ("Не рекомендован к зачислению")
        self.layout.addWidget (self.setUnsuccessButton )
        self.setUnsuccessButton.clicked.connect (self.unsuccessStudent)

    def successStudent (self):
        try:
            connect.setSucces ( self.student[1], self.gradetype_id, True )
            self.close ()
            self.function ()
        except Exception as err:
            print ( "ERROR: on setting mark" )
            print ( err )

    def unsuccessStudent (self):
        try:
            connect.setSucces ( self.student[1], self.gradetype_id, False )
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
            studentButton = QPushButton ( student["student_name"] )
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
 
        self.setMark = SetMarkWidget ( self.examData[0], self.examData[1], sender.data, lambda: self.endExam () if self.isFinal () else None )        
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


class examsManage ( QWidget ):
    def __init__ ( self ):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.layout.addWidget ( QLabel ("Управления экзаменами") )
        self.setWindowTitle ("Управление экзаменами")

        self.cabinets = connect.getExamGradetype ()
        self.tableWidget = tableWidget ( headers = ["Название экзамена", "ID Экзамена", "Название профиля", "ID профиля", "Профильный(Да/Нет)"], columns = self.cabinets, vertical = False)
        self.layout.addWidget (self.tableWidget)
        self.insertCabinetButton = QPushButton ("Добавить экзамен")
        self.insertCabinetButton.clicked.connect ( self.insertCabinet )
        self.layout.addWidget ( self.insertCabinetButton )
        self.deleteExamCabinet = QPushButton ("Удалить экзамен")
        self.deleteExamCabinet.clicked.connect ( self.deleteCabinet )
        self.layout.addWidget ( self.deleteExamCabinet )

    def refresh (self):
        self.cabinets = connect.getExamGradetype ()
        self.tableWidget.setTable ( self.cabinets, False )

    def insertCabinet ( self ):
        self.insertCabinetWindow = insertExamGradetype ( function = lambda: self.refresh() )
        self.insertCabinetWindow.show()

    def deleteCabinet ( self ):
        self.insertCabinetWindow = deleteExamGradetype (function = lambda: self.refresh())
        self.insertCabinetWindow.show()


class mainMenu ( QWidget ):
    def __init__ (self, teacher_id):
        super (QWidget, self).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.resize (300, 300)

        self.teacher = connect.getTeacher ( teacher_id = teacher_id )
        self.layout.addWidget ( QLabel ( str ( self.teacher[0][1]) ) )
        self.setWindowTitle ("Меню учителя")
        self.layout.addWidget ( QLabel ("Меню учителя:") )

        self.examsetManageButton = QPushButton ( "Сформировать связки экзаменов" )
        self.layout.addWidget (self.examsetManageButton ) 
        self.cabinetsButton = QPushButton ( "Управление кабинетами" )
        self.cabinetsButton.clicked.connect ( self.cabinetsManage )
        self.layout.addWidget ( self.cabinetsButton )
        self.makeExamButton = QPushButton ( "Провести экзамен" )
        self.layout.addWidget (self.makeExamButton )
        self.makeExamButton.clicked.connect ( self.makeExam )
        self.formListsButton = QPushButton ( "Сформировать екзамены" )
        self.formListsButton.clicked.connect ( self.makeExamLists )
        self.layout.addWidget ( self.formListsButton )
        self.examsetManageButton.clicked.connect (self.examsManage)
        self.checkResultsButton = QPushButton ( "Списки по экзаменам" )
        self.checkResultsButton.clicked.connect ( self.getResults )
        self.layout.addWidget (self.checkResultsButton )
        self.getGroupsButton = QPushButton ( "Сформировать группы для зачисления" )
        self.getGroupsButton.clicked.connect ( self.getGroups )
        self.layout.addWidget (self.getGroupsButton )

        self.exitButton = QPushButton ( "Выйти из приложения" )
        self.exitButton.clicked.connect ( self.close )
        self.layout.addWidget (self.exitButton )
        self.exitButton.setStyleSheet ("color: rgb(255, 178, 178);")

    def examsManage (self):
        self.examManageWindow = examsManage ()
        self.examManageWindow.show()

    def makeExamLists ( self ):
        self.examListsWindow = makeExamList ()
        self.examListsWindow.show ()

    def cabinetsManage ( self ):
        self.cabinetsManageWindow = cabinetsManage ()
        self.cabinetsManageWindow.show()

    def getResults (self):
        self.examLists = showExamLists ()
        self.examLists.show ()

    def makeExam ( self ):
        self.exam = Exam ()
        self.exam.show()

    def getGroups ( self ):
        self.groups = makeGroups ()
        self.groups.show()


class main ():
    def __init__ (self):
        self.app = QApplication ( sys.argv )
        global DB_ERROR
        if DB_ERROR:
            self.errorWindow = errorWindow ()
            self.errorWindow.errorTemplate ("Ошибка при подключении к базе данных.\nУведомите об этом администратора.")
            self.errorWindow.show ()
        else:
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
