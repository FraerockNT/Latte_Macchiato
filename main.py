import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from PyQt6.uic import loadUi


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None, coffee_id=None):
        super().__init__(parent)
        loadUi('addEditCoffeeForm.ui', self)
        self.coffee_id = coffee_id
        self.saveButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.close)

        if self.coffee_id:
            self.load_data()

    def load_data(self):
        conn = sqlite3.connect('../data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        coffee_data = cursor.fetchone()
        conn.close()

        if coffee_data:
            self.nameInput.setText(coffee_data[1])
            self.roastLevelInput.setText(coffee_data[2])
            self.groundOrBeansInput.setText(coffee_data[3])
            self.tasteDescriptionInput.setText(coffee_data[4])
            self.priceInput.setText(str(coffee_data[5]))
            self.packageVolumeInput.setText(str(coffee_data[6]))

    def save_data(self):
        name = self.nameInput.text()
        roast_level = self.roastLevelInput.text()
        ground_or_beans = self.groundOrBeansInput.text()
        taste_description = self.tasteDescriptionInput.text()
        price = self.priceInput.text()
        package_volume = self.packageVolumeInput.text()

        if not all([name, roast_level, ground_or_beans, price, package_volume]):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        conn = sqlite3.connect('../data/coffee.sqlite')
        cursor = conn.cursor()

        if self.coffee_id:
            cursor.execute('''
                UPDATE coffee
                SET name = ?, roast_level = ?, ground_or_beans = ?, taste_description = ?, price = ?, package_volume = ?
                WHERE id = ?
            ''', (name, roast_level, ground_or_beans, taste_description, price, package_volume, self.coffee_id))
        else:
            cursor.execute('''
                INSERT INTO coffee (name, roast_level, ground_or_beans, taste_description, price, package_volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, roast_level, ground_or_beans, taste_description, price, package_volume))

        conn.commit()
        conn.close()
        self.accept()


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.load_data()
        self.addButton.clicked.connect(self.open_add_form)
        self.editButton.clicked.connect(self.open_edit_form)

    def load_data(self):
        conn = sqlite3.connect('../data/coffee.sqlite')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(7)

        for i, row in enumerate(rows):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

        conn.close()

    def open_add_form(self):
        form = AddEditCoffeeForm(self)
        if form.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    def open_edit_form(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a row to edit!")
            return

        coffee_id = self.tableWidget.item(selected_row, 0).text()
        form = AddEditCoffeeForm(self, coffee_id)
        if form.exec() == QDialog.DialogCode.Accepted:
            self.load_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())