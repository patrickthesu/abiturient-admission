from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGroupBox, QFrame
from PyQt6.QtCore import pyqtSlot
from .errors import errorWindow
import sys
import os

class isolatedWidget ( QFrame ):
    def __init__( self ):
        super ( QFrame, self ).__init__()

        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

class selectWidget (isolatedWidget):
    def __init__( self, path = os.getcwd(), function = lambda text: print ( text )):
        super ( QWidget, self ).__init__()

        self.function = function
        self.path = path

        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout ) 
        self.setWindowTitle ( path )

        self.listdir = isolatedWidget ()
        self.headerLabel = QLabel ( path )
        self.layout.addWidget ( self.headerLabel )
        font = self.headerLabel.font ()
        font.setBold(True)
        self.listdir.setFont(font)

        self.selected = QLabel ( "Нет" )
        self.selected.layout = QHBoxLayout ()
        self.selected.layout.addWidget ( QLabel ( "Выбраный файл:" ) )
        self.selected.layout.addWidget ( self.selected )

        self.layout.addLayout ( self.selected.layout )

        self.layout.addWidget ( self.listdir )

        self.listdir.setStyleSheet ( "background-color: rgba(0,0,0,0.2);\nborder-radius:10px\n" )

        self.downdButton = QPushButton ( ".." )
        self.downdButton.setStyleSheet ( "border:none;\nborder-radius:5px;\npadding: 3px;\ncolor:rgb(192, 192, 255);\nbackground-color: none" )
        self.downdButton.clicked.connect ( self.downd )
        self.listdir.layout.addWidget ( self.downdButton )

        
        self.focusedWidget = QPushButton ()
        self.focus = None

        self.fillListdir ()

        self.returnFileName = ""

    def downd ( self ):
        self.path = self.path.split("/")
        self.path.pop()
        
        if len ( self.path ) == 1: self.path = "/"
        else: self.path = "/".join( self.path )

        print ( self.path )

        os.chdir ( self.path )
        self.headerLabel.setText ( self.path )
        self.fillListdir ()

    def fillListdir ( self ):

        try:
            for button in self.filelist: 
                button.hide()
        except:
            print ( "Filling select widget at first time" )

        self.filelist = []

        with os.scandir(self.path) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    self.filelist.append ( QPushButton ( entry.name ) )
                    styleSheets = "border:none;\nborder-radius:5px;\npadding: 3px;\nbackground-color: none;"
                    self.listdir.layout.addWidget ( self.filelist[len(self.filelist) - 1] )
                    if ( entry.is_dir() ):
                        styleSheets += "\ncolor:rgb(192, 192, 255);" 
                        font = self.filelist[len(self.filelist) - 1].font()
                        font.setBold(True)
                        self.filelist[len(self.filelist) - 1].setFont(font)
                        self.filelist[len(self.filelist) - 1].clicked.connect ( self.chdir )
                    else: 
                        if self.focus == self.path + "/" + entry.name: styleSheets += "\nbackground-color:rgba(192,192,192,0.3);" 
                        self.filelist[len(self.filelist) - 1].clicked.connect ( self.changeFocus ) 
                    self.filelist[len(self.filelist) - 1].setStyleSheet ( styleSheets )

 
        self.function = self.function

    @pyqtSlot()
    def changeFocus ( self ):
        self.focus = self.path + "/" + self.sender().text() 

        self.focusedWidget = self.sender
        self.selected.setText ( self.sender().text() ) 
        self.fillListdir ()
        
        try:
            with open ( self.focus, "r" ) as file:
                self.function ( file.read() )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print ( exc_type, fname, exc_tb.tb_lineno )
            self.e = errorWindow()
            self.e.show()
           
    @pyqtSlot()
    def chdir ( self ):
        try:
            os.chdir ( "./" + self.sender().text() )
        except:
            self.e = errorWindow()
            self.e.show()

        self.path = os.getcwd () 
        self.fillListdir ()
            
    def __call__ (self):
        return self.returnFileName


class writeWidget ( QWidget ): 
    def __init__( self, path = os.getcwd(), function = lambda: print ( "write here" ), writeFunction = None):
        super ( QWidget, self ).__init__()

        self.function = function
        self.writeFunction = writeFunction
        self.path = path

        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout ) 
        self.setWindowTitle ( path )

        self.listdir = isolatedWidget ()
        self.headerLabel = QLabel ( path )
        self.layout.addWidget ( self.headerLabel )
        font = self.headerLabel.font ()
        font.setBold(True)
        self.listdir.setFont(font)

        self.selected = QLabel ( "Нет" )
        self.selected.layout = QHBoxLayout ()
        self.selected.layout.addWidget ( QLabel ( "Записать под именем:" ) )
        self.selected.layout.addWidget ( self.selected )

        self.layout.addLayout ( self.selected.layout )

        self.layout.addWidget ( self.listdir )

        self.listdir.setStyleSheet ( "background-color: rgba(0,0,0,0.2);\nborder-radius:10px\n" )

        self.downdButton = QPushButton ( ".." )
        self.downdButton.setStyleSheet ( "border:none;\nborder-radius:5px;\npadding: 3px;\ncolor:rgb(192, 192, 255);\nbackground-color: none" )
        self.downdButton.clicked.connect ( self.downd )
        self.listdir.layout.addWidget ( self.downdButton )

        
        self.focusedWidget = QPushButton ()
        self.focus = None

        self.fillListdir ()

        self.layout.addWidget ( QLabel ( "Введите имя файла:" ) )

        self.filenameInput = QLineEdit () 
        self.layout.addWidget ( self.filenameInput )
        self.filenameInput.textChanged.connect ( self.setNewFileFocus )

        self.returnFileName = ""

        self.writeButton = QPushButton ( "Записать файл" )

        self.writeButton.clicked.connect ( self.write )

        self.layout.addWidget ( self.writeButton )

    def downd ( self ):
        self.path = self.path.split("/")
        self.path.pop()
        
        if len ( self.path ) == 1: self.path = "/"
        else: self.path = "/".join( self.path )

        print ( self.path )

        os.chdir ( self.path )
        self.headerLabel.setText ( self.path )
        self.fillListdir ()

    def fillListdir ( self ):

        try:
            for button in self.filelist: 
                button.hide()

        except:
            print ( "Filling select widget at first time" )

        self.filelist = []

        with os.scandir(self.path) as it:
            for entry in it:
                if not entry.name.startswith('.'):
                    self.filelist.append ( QPushButton ( entry.name ) )
                    styleSheets = "border:none;\nborder-radius:5px;\npadding: 3px;\nbackground-color: none;"
                    self.listdir.layout.addWidget ( self.filelist[len(self.filelist) - 1] )
                    if ( entry.is_dir() ):
                        styleSheets += "\ncolor:rgb(192, 192, 255);" 
                        font = self.filelist[len(self.filelist) - 1].font()
                        font.setBold(True)
                        self.filelist[len(self.filelist) - 1].setFont(font)
                        self.filelist[len(self.filelist) - 1].clicked.connect ( self.chdir )
                    else: 
                        if self.focus == self.path + "/" + entry.name: styleSheets += "\nbackground-color:rgba(192,192,192,0.3);" 
                        self.filelist[len(self.filelist) - 1].clicked.connect ( self.changeFocus ) 
                    self.filelist[len(self.filelist) - 1].setStyleSheet ( styleSheets )

 

    @pyqtSlot()
    def changeFocus ( self ):
        self.focus = self.path + "/" + self.sender().text() 

        self.focusedWidget = self.sender
        self.selected.setText ( self.sender().text() ) 
        self.fillListdir ()        

        self.filenameInput.setText ( self.focus.split("/")[-1] )


    def setNewFileFocus ( self ):
        self.focus = self.path + "/" + self.filenameInput.text () 

        self.focusedWidget = None
        self.fillListdir()

    @pyqtSlot()
    def chdir ( self ):
        savedFilename = self.path.split("/").pop ()

        try:
            os.chdir ( "./" + self.sender().text() )
        except:
            self.e = errorWindow()
            self.e.show()

        self.focus = os.getcwd() + "/" + savedFilename
        self.path = os.getcwd () 
        self.fillListdir ()
 
    
    def write ( self ):
        if self.writeFunction:
            self.writeFunction (self.focus, index = False)
            return True

        try:
            with open ( self.focus , "w" ) as f:
                f.write ( self.function() )
        except:
            self.e = errorWindow()
            self.e.show()            

        self.fillListdir ()
 
           
    def __call__ (self):
        return self.returnFileName


class fileWriteWidget (QWidget):
    def __init__ ( self, function = lambda : "Output text" ):
        
        super ( QWidget, self ).__init__()

        self.function = function
        
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.layout.addWidget ( QLabel ( "Введите имя файла:" ) )

        self.filenameInput = QLineEdit ()
        
        self.layout.addWidget ( self.filenameInput )

        self.writeButton = QPushButton ( "Записать" )
        self.writeButton.clicked.connect ( self.write )

        self.layout.addWidget ( self.writeButton )

    def write ( self ):
        try:
            with open ( self.filenameInput.text().strip(), "w" ) as f:
                f.write ( self.function() )
        except:
            self.e = errorWindow()
            self.e.show()            
