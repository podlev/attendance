import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow, QWidget
import sqlite3

con = sqlite3.connect('database.db')


class GroupWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('group.ui', self)
        self.loadTable()

    def loadTable(self):
        connect = sqlite3.connect('database.db')
        cur = connect.cursor()
        result = cur.execute("""SELECT * FROM groups""").fetchall()
        self.tableWidget.setColumnCount(len(result[0]) - 1)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(('id', 'ФИО', 'Группа'))
        self.tableWidget.setVerticalHeaderLabels([str(i[0]) for i in result])
        for i, row in enumerate(result):
            for j, elem in enumerate(row[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

        for elem in result:
            print(elem)
        connect.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('design.ui', self)
        self.test_button.clicked.connect(self.loadTable)
        self.group_button.clicked.connect(self.groupEdit)

    def loadTable(self):
        connect = sqlite3.connect('database.db')
        cur = connect.cursor()
        students = cur.execute("""SELECT * FROM students""").fetchall()
        groups = cur.execute("""SELECT * FROM groups""").fetchall()
        self.tableWidget.setColumnCount(len(students[0]))
        self.tableWidget.setRowCount(len(students))
        self.tableWidget.setHorizontalHeaderLabels(('id', 'ФИО', 'Группа'))
        self.tableWidget.setVerticalHeaderLabels([str(i[0]) for i in students])
        for i, row in enumerate(students):
            for j, elem in enumerate(row[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

        for elem in students:
            print(elem)
        connect.close()

    def groupEdit(self):
        self.groups = GroupWindow()
        self.groups.show()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
