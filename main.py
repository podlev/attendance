import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow, QWidget
import sqlite3

connect = sqlite3.connect('database.db')
cursor = connect.cursor()


class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('students_design.ui', self)


class GroupWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('group_design.ui', self)
        self.add_button.clicked.connect(self.addGroup)
        self.delete_button.clicked.connect(self.delGroup)
        self.loadTable()

    def loadTable(self):
        result = cursor.execute("""SELECT group_name FROM groups""").fetchall()
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setHorizontalHeaderLabels(('Группа', ))
        self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(result) + 1)])
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def addGroup(self):
        cursor.execute("""INSERT INTO groups(group_name) VALUES(?)""", (self.group_edit.text(),))
        self.group_edit.clear()
        connect.commit()
        self.loadTable()

    def delGroup(self):
        result = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 0).data()
        cursor.execute("""DELETE FROM groups WHERE group_id=(?)""", (result,))
        connect.commit()
        self.loadTable()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.students = StudentWindow()
        self.groups = GroupWindow()
        uic.loadUi('design.ui', self)
        self.test_button.clicked.connect(self.loadTable)
        self.group_button.clicked.connect(self.groupEdit)
        self.student_button.clicked.connect(self.studentEdit)

    def loadTable(self):
        students = cursor.execute(
            """SELECT name, group_name 
            FROM students, groups 
            WHERE students.group_id = groups.group_id""").fetchall()
        self.tableWidget.setColumnCount(len(students[0]))
        self.tableWidget.setRowCount(len(students))
        self.tableWidget.setHorizontalHeaderLabels(('ФИО', 'Группа'))
        self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(students) + 1)])
        for i, row in enumerate(students):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

        for elem in students:
            print(elem)

    def groupEdit(self):
        self.groups.show()

    def studentEdit(self):
        self.students.show()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
