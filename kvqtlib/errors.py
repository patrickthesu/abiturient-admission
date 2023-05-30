from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout

class errorWindow ( QWidget ):
    def __init__ ( self ):
        super ( QWidget, self ).__init__()
 
        self.setWindowTitle ( "Ошибка" )

        self.layout = QVBoxLayout ()
        self.setLayout( self.layout )

        self.messageLabel = QLabel ( "Что-то пошло не так =(" )
        self.layout.addWidget ( self.messageLabel )
        
        self.okButton = QPushButton ( "Ок" )
        self.layout.addWidget ( self.okButton )

        self.okButton.clicked.connect ( self.hide )


    def errorTemplate ( self, text ):
        self.messageLabel.setText ( text )
        
        self.show()

    def infinityError ( self ):
        self.errorTemplate ( "Вы создали бесконечный цикл." )

    def stepIsZeroError ( self ): 
        self.errorTemplate( "Вы ввели значение равное нулю." )

    def emptyInputError ( self ):
        self.errorTemplate( "Вы ввели пустой массив." )

    def IOFError ( self ):
        self.errorTemplate( "Диапазон вне массива." )

    def incorrectValueError ( self ):
        self.errorTemplate( "Вы ввели некоректное значение.\nПожалуйста, будьте внимательнее." )

    def ZEXError ( self ):
        self.errorTemplate( "Вы ввели отрицательные значения." )

#ew = errorWindow ()

         
