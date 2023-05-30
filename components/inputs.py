from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit

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

class phoneEdit (QWidget):
    def __init__ ( self ):
        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.edit = QLineEdit ()
        self.edit.textChanged.connect (self.check)
        self.layout.addWidget ( self.edit )

        self.error = QLabel ("Неправильный номер")
        self.error.setStyleSheet ( "color: red;" )
        self.layout.addWidget (self.error)
        self.error.hide ()

    def check (self):
        self.error.hide ()
        if self.edit.text().strip() != self.edit.text():
            self.edit.setText(self.edit.text().strip())

        if len(self.edit.text().strip()) > 0 and self.edit.text()[0] == '+' and len ( self.edit.text() ) >= 9:
            try:
                int ( self.edit.text ()[1:] )
                return True
            except:
                pass
        
        self.error.show()
        return False

    def __call__ (self):
        if self.check ():
            return self.edit.text ()
        else: return False

class adressEdit (QWidget):
    def __init__ ( self ):

        super ( QWidget, self ).__init__()
        self.layout = QVBoxLayout ()
        self.setLayout ( self.layout )
        
        self.edit = QLineEdit ()
        self.edit.editingFinished.connect (self.check)
        self.layout.addWidget ( self.edit )

        self.error = QLabel ("Неправильный адрес")
        self.error.setStyleSheet ( "color: red;" )
        self.layout.addWidget (self.error)
        self.error.hide ()

    def check (self):
        self.error.hide ()
        if self.edit.text().strip() != self.edit.text():
            self.edit.setText(self.edit.text().strip())
        return True

    def __call__ (self):
        if self.check ():
            return self.edit.text ()
        return False


