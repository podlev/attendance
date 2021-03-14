import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow, QWidget, QMessageBox, QFileDialog
import sqlite3
import csv

connect = sqlite3.connect('database.db')
cursor = connect.cursor()


class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('students_design.ui', self)
        self.add_button.clicked.connect(self.addStudent)
        self.delete_button.clicked.connect(self.deleteStudent)
        self.import_button.clicked.connect(self.importStudents)

        # Загрузка списка групп в фильтр
        result = cursor.execute("""SELECT group_name, group_id FROM groups""").fetchall()
        self.groups_list = dict(result)
        self.group_filter.clear()
        self.group_filter.addItems(['Без фильтра'] + list(self.groups_list.keys()))

        # Загрузка списка групп в выпадающий список
        self.group_edit.addItems(list(self.groups_list.keys()))

        # Загрузка таблицы
        self.loadTable()
        self.group_filter.activated.connect(self.loadTable)

    def loadTable(self):
        if str(self.group_filter.currentText()) == 'Без фильтра':
            result = cursor.execute(
                """SELECT student_name, group_name, student_id 
                FROM students, groups 
                WHERE students.group_id = groups.group_id""").fetchall()
        else:
            result = cursor.execute(
                """SELECT student_name, group_name, student_id 
                FROM students, groups 
                WHERE students.group_id = groups.group_id
                and groups.group_id = (?)""", (self.groups_list[str(self.group_filter.currentText())],)).fetchall()
        # Проверка на пустую группу
        if result:
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setHorizontalHeaderLabels(('ФИО', 'Группа', 'id'))
            self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(result) + 1)])
            for i, row in enumerate(result):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
            self.tableWidget.resizeColumnsToContents()
        else:
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(1)
            self.tableWidget.setHorizontalHeaderLabels(('ФИО', 'Группа', 'id'))
            self.tableWidget.setVerticalHeaderLabels(('1',))
            for i in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(0, i, QTableWidgetItem(' '))

    def addStudent(self):
        print(str(self.group_edit.currentText()))
        cursor.execute("""INSERT INTO students(student_name, group_id) VALUES(?, ?)""",
                       (self.student_edit.text(), self.groups_list[str(self.group_edit.currentText())]))
        self.student_edit.clear()
        connect.commit()
        self.loadTable()

    def deleteStudent(self):
        message = QMessageBox.question(self, 'Удалить студента', "Вы уверены?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            result = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 2).data()
            cursor.execute("""DELETE FROM students WHERE student_id=(?)""", (result,))
            connect.commit()
            self.loadTable()

    def importStudents(self):
        file = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        try:
            with open(file, encoding='utf8') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                for row in reader:
                    print(row['student_name'], row['group_id'])
                    cursor.execute("""INSERT INTO students(student_name, group_id) VALUES(?, ?)""",
                                   (row['student_name'], row['group_id']))
                    connect.commit()
            self.loadTable()
        except:
            message = QMessageBox()
            message.setIcon(3)
            message.setText('Ошибка файла')
            message.exec()


class GroupWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('group_design.ui', self)
        self.add_button.clicked.connect(self.addGroup)
        self.delete_button.clicked.connect(self.deleteGroup)
        self.loadTable()

    def loadTable(self):
        result = cursor.execute("""SELECT group_name, group_id FROM groups""").fetchall()
        if result:
            self.tableWidget.setColumnCount(len(result[0]))
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setHorizontalHeaderLabels(('Группа', 'id'))
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

    def deleteGroup(self):
        message = QMessageBox.question(self, 'Удалить группу', "Вы уверены?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if message == QMessageBox.Yes:
            result = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 1).data()
            cursor.execute("""DELETE FROM groups WHERE group_id=(?)""", (result,))
            connect.commit()
            self.loadTable()


class AttendanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('attendance_design.ui', self)
        # Загрузка списка групп в выпадающий список
        result = cursor.execute("""SELECT group_name, group_id FROM groups""").fetchall()
        self.groups_list = dict(result)
        self.group_edit.clear()
        self.group_edit.addItems(list(self.groups_list.keys()))
        self.add_attendance.clicked.connect(self.addAttendance)
        # Загрузка таблицы или по обновлению группы или обновлению даты
        self.calendarWidget.clicked.connect(self.loadTable)
        self.group_edit.activated.connect(self.loadTable)

    def loadTable(self):
        self.date = self.calendarWidget.selectedDate().toString('dd.MM.yyyy')
        result = cursor.execute(
            """SELECT student_name, student_id 
            FROM students
            WHERE group_id = (?)""", (self.groups_list[str(self.group_edit.currentText())],)).fetchall()
        self.student_list = dict(result)
        # Проверка на пустую группу
        if result:
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(len(self.student_list))
            self.tableWidget.setHorizontalHeaderLabels(('ФИО', self.date))
            self.tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len(self.student_list) + 1)])
            for i, name in enumerate(self.student_list):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(name)))
                # Присутствией по умолчанию
                self.tableWidget.setItem(i, 1, QTableWidgetItem('+'))
            self.tableWidget.resizeColumnsToContents()
        # Добавить всплывашку если группа пустая
        else:
            message = QMessageBox.question(self, 'Группа пустая', "Добавить студентов в группу?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if message == QMessageBox.Yes:
                self.students = StudentWindow()
                self.students.show()

    def addAttendance(self):
        message = QMessageBox.question(self, 'Посещаемость', "Выставить посещаемость?",
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if message == QMessageBox.Yes:
            for i in range(self.tableWidget.rowCount()):
                if self.tableWidget.model().index(i, 1).data() == '+':
                    cursor.execute("""INSERT INTO attendance(date, student_id, state) VALUES(?, ?, ?)""",
                                   (self.date, self.student_list[self.tableWidget.model().index(i, 0).data()], 1))
                    connect.commit()
                else:
                    cursor.execute("""INSERT INTO attendance(date, student_id, state) VALUES(?, ?, ?)""",
                                   (self.date, self.student_list[self.tableWidget.model().index(i, 0).data()], 0))
                    connect.commit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('design.ui', self)
        self.group_button.clicked.connect(self.groupEdit)
        self.student_button.clicked.connect(self.studentEdit)
        self.attendance_button.clicked.connect(self.attendanceEdit)

        self.group_edit.activated.connect(self.loadTable)
        # Загрузка списка групп в выпадающий список
        result = cursor.execute("""SELECT group_name, group_id FROM groups""").fetchall()
        self.groups_list = dict(result)
        self.group_edit.clear()
        self.group_edit.addItems(list(self.groups_list.keys()))
        self.loadTable()

    def loadTable(self):

        # Выбранная група для загрузки
        select_group = self.groups_list[str(self.group_edit.currentText())]

        # Получение списка дат
        dates = cursor.execute(
            """SELECT date 
            FROM attendance, students 
            WHERE attendance.student_id = students.student_id 
            AND students.group_id = (?)""", (select_group,)).fetchall()
        dates = sorted(list(set([i[0] for i in dates])))
        # Установка количества столбцов
        self.tableWidget.setColumnCount(len(dates) + 1)
        self.tableWidget.setHorizontalHeaderLabels((['ФИО'] + [str(i) for i in dates]))
        # Получение списка студентов
        students = cursor.execute(
            """SELECT student_name 
            FROM attendance, students 
            WHERE attendance.student_id = students.student_id 
            AND students.group_id = (?)""", (select_group,)).fetchall()
        students = sorted(list(set([i[0] for i in students])))
        self.tableWidget.setRowCount(len(students))
        self.tableWidget.setVerticalHeaderLabels([str(i + 1) for i in range(len(students))])
        for i in range(len(students)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(str(students[i])))
        self.tableWidget.resizeColumnsToContents()

        for i in range(self.tableWidget.rowCount()):
            for j in range(1, self.tableWidget.columnCount()):
                result = cursor.execute(
                    """SELECT state 
                    FROM attendance, students 
                    WHERE attendance.student_id = students.student_id 
                    AND students.group_id = (?) AND student_name = (?) AND date = (?)""",
                    (select_group, self.tableWidget.model().index(i, 0).data(), dates[j - 1])).fetchall()
                if result[0][0]:
                    self.tableWidget.setItem(i, j, QTableWidgetItem('+'))
                else:
                    self.tableWidget.setItem(i, j, QTableWidgetItem('-'))

    def groupEdit(self):
        self.groups = GroupWindow()
        self.groups.show()

    def studentEdit(self):
        self.students = StudentWindow()
        self.students.show()

    def attendanceEdit(self):
        self.attendance = AttendanceWindow()
        self.attendance.show()


app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec_())
