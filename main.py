import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow
import sqlite3

con = sqlite3.connect('database.db')


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.test_button.clicked.connect(self.loadTable)

    def loadTable(self):
        connect = sqlite3.connect('database.db')
        cur = connect.cursor()
        result = cur.execute("""SELECT * FROM students""").fetchall()
        self.tableWidget.setColumnCount(len(result[0]) - 1)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(('ФИО', 'Группа'))
        self.tableWidget.setVerticalHeaderLabels([str(i[0]) for i in result])
        for i, row in enumerate(result):
            for j, elem in enumerate(row[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

        for elem in result:
            print(elem)
        connect.close()


app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
