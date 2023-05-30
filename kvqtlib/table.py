from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QWidget, QHBoxLayout, QHeaderView

class tableWidget ( QWidget ):
    def setTable ( self, columns, vertical = True ):
        if vertical:
            self.table.setColumnCount ( len ( columns ) )
            self.table.setRowCount ( len ( columns[0] ) )
        else:
            self.table.setColumnCount ( len ( columns[0] ) )
            self.table.setRowCount ( len ( columns ) )

        for i in range ( 0, len ( columns ) ):
            for itemI in range ( 0, len ( columns[i] ) ):
                if vertical:
                    self.table.setItem ( itemI, i, QTableWidgetItem ( str ( columns[i][itemI] ) ) )  
                else:
                    self.table.setItem ( i, itemI, QTableWidgetItem ( str ( columns[i][itemI] ) ) )  

        self.layout.addWidget ( self.table )
 

    def __init__ ( self, headers = [], columns = [[]], title = "Таблица", vertical = True ):
        super ( QWidget, self ).__init__ ()
        self.w = 300
        self.h = 400

        self.layout = QHBoxLayout ()

        self.table = QTableWidget ()

        self.setTable ( columns, vertical )

        for i in range ( 0, len ( headers ) ):
             self.table.setHorizontalHeaderItem ( i, QTableWidgetItem ( headers[i] ) )       

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.setLayout ( self.layout )
        self.setWindowTitle ( title )

