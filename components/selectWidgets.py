from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, QCheckBox, QScrollArea, QPushButton
from PyQt6.QtCore import pyqtSlot

class searchWidget (QWidget):
    def __init__ (self):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout(self.layout)

        self.errorLabel = QLabel ( "Элемент не выбран" )
        self.errorLabel.setStyleSheet ( "color: red;" )
        self.layout.addWidget (self.errorLabel)
        self.errorLabel.hide ()

        self.searchLine = QLineEdit ()
        self.searchLine.textChanged.connect (self.search)
        self.layout.addWidget (self.searchLine)

        self.scrollLayout = QVBoxLayout ()
        self.scrollLayoutWidget = QWidget ()
        self.scrollLayoutWidget.setLayout (self.scrollLayout)

        self.scrollArea = QScrollArea ()
        self.scrollArea.setMinimumHeight(150)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget (self.scrollLayoutWidget)
        self.layout.addWidget (self.scrollArea)

        self.buttons = []
        self.selected = None
    
        

    def addItem (self, text, additionalText): 
        selectButton = QPushButton()
        selectButton.setText (text.strip())
        selectButton.additionalText = additionalText
        selectButton.clicked.connect (self.select)
        self.buttons.append(selectButton)
        self.scrollLayout.addWidget(selectButton)
        self.fillLayout ()

    def fillLayout (self, mask = None):
        for i in range(len(self.buttons)):
            styleSheets = "border:none;\nborder-radius:5px;\npadding: 3px;\nbackground-color: none;"
            if self.selected == self.buttons[i]:
                styleSheets += "\nbackground-color:rgba(192,192,192,0.3);"
            else: self.buttons[i].hide()

            if mask == None or mask.lower() in self.buttons[i].text().lower():
                #print (f"mask: '{mask}', text: '{self.buttons[i].text()}'")
                self.buttons[i].show ()
            self.buttons[i].setStyleSheet(styleSheets)

    def check (self):
        self.errorLabel.hide ()
        print (123)
        if not self.selected: return error()
        print (321)
        return True

    def error (self, text):
        self.errorLabel.setText (text)
        self.errorLabel.show ()
        return False

    @pyqtSlot ()
    def select (self):
        self.selected = self.sender()
        self.searchLine.setText (self.selected.text())
        #self.fillLayout ()

    def currentData (self):
        if self.check (): return self.selected.additionalText
        return False
         
    def search (self):
        searchText = self.searchLine.text().strip()
        if searchText == "": self.fillLayout ()
        else: self.fillLayout (searchText)

class languageEdit (QLineEdit):
    def __init__ (self):
        super ( QWidget, self ).__init__()
        self.textChanged.connect (self.check)

    def check (self):
        if self.text().strip() != self.text():
            self.setText(self.text().strip())

class languagesInput (QWidget):
    def __init__ (self):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.inputs = [languageEdit()]
        self.reload ()

    def reload (self):
        for inp in self.inputs:
            self.layout.addWidget (inp)

    def addNewLanguage (self):
        if self.inputs[-1].text() == "":
            return False
        self.inputs.append ( languageEdit() )
        self.reload()

class languageSelect (QWidget):
    def __init__ (self, connect):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.primaryList = searchWidget ()
        self.foreignList = searchWidget ()
        #self.primaryList.currentIndexChanged.connect (self.check)
        #self.foreignList.currentIndexChanged.connect (self.check)
        self.layout.addWidget ( QLabel ("Ваш основной язык:") )
        self.layout.addWidget ( self.primaryList )
        self.layout.addWidget ( QLabel ("Иностранный язык:") )
        self.layout.addWidget ( self.foreignList )
        self.errorLabel = QLabel ( "Языки одинаковые" )
        self.errorLabel.setStyleSheet ( "color: red;" )
        self.layout.addWidget ( self.errorLabel )
 
        for language in connect.getLanguages ():
            self.primaryList.addItem ( language[2], language[0] )
            self.foreignList.addItem ( language[2], language[0] )

        self.errorLabel.hide()

    def error (self, text):
        self.errorLabel.setText (text)
        self.errorLabel.show ()
        return False


    def check (self):
        self.errorLabel.hide()
        try:
            if self.primaryList.currentData() == self.foreignList.currentData(): return self.error ( "Языки не могут быть одинаковыми" )
        except Exception as err:
            print (err)
            return False
        return True

    def __call__ (self):
        print (self.check())
        if not self.check ():
            return False

        try:
            if self.primaryList.currentData() != self.foreignList.currentData():return { 
                "primary_id" : self.primaryList.currentData(),
                "foreign_id" : self.foreignList.currentData()
               }
        except Exception as err:
            print ( "ERROR: language select error" )
            print (err)
        return False



class schoolSelect (QWidget):
    def __init__ (self, connect):
        super ( QWidget, self ).__init__()
        self.connect = connect
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )

        self.citiesList = QComboBox ()
        self.layout.addWidget ( self.citiesList )

        for city in self.connect.getCities ():
            self.citiesList.addItem (city[1], userData = city[0])

        self.citiesList.currentIndexChanged.connect ( self.cityChanged )
        self.schoolLabel = QLabel ( "Выберите вашу школу" )
        self.layout.addWidget ( self.schoolLabel )
        self.schoolLabel.hide()
        self.errorLabel = QLabel ( "Вы не выбрали школу" )
        self.errorLabel.setStyleSheet ( "color: red;" )
        self.layout.addWidget ( self.errorLabel )
        self.errorLabel.hide()

    def cityChanged (self):
        self.errorLabel.hide()
        try:
            self.schoolList.hide()
        except:
            pass
        self.schoolLabel.show()
        self.schoolList = QComboBox ()
        for school in self.connect.getSchools ( self.citiesList.currentData() ): 
            self.schoolList.addItem (school[1], userData = school[0])
        self.layout.addWidget (self.schoolList)

    def __call__ (self):
        self.errorLabel.hide()
        try:
            if self.schoolList: return {"school_id": self.schoolList.currentData()}
        except Exception as err:
            print ("ERROR: school select error")
            print ( err )
            self.errorLabel.show()
        return False 


