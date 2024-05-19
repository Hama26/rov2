from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QTextEdit, QHBoxLayout, QComboBox, QInputDialog , QHeaderView
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from optimization_solver import solve_knapsack, solve_production
import sys


class OptimizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.insertedColumns = 0
        # Main window setup
        self.setWindowTitle("Optimization Solver")
        self.setGeometry(200, 200, 1000, 600)
        self.setFont(QFont("Roboto", 6))
        # Set background image
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Add a background image
        self.background_label = QLabel(self.central_widget)
        background_image = QPixmap("./image.jpg")  # Replace with the path to your image
        self.background_label.setPixmap(background_image.scaled(300, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Adjust size as needed
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setGeometry(250, -60, 500, 300) 
        self.setStyleSheet("""
            QMainWindow { background-color: white; }
            QPushButton { background-color: #0078d7; color: white; font-size: 10pt; border-radius: 5px; }
            QPushButton:hover { background-color: #005fa3; }
            QLabel, QLineEdit, QTextEdit, QComboBox { font-size: 10pt; }
            QLabel { font-size: 10pt; }
            QTextEdit { background-color: #ffffff; }
            QLineEdit { border-radius: 3px; padding: 2px; background-color: #ffffff; }
            QPushButton.solve-button { background-color: coral; color: white; }
            QPushButton.solve-button:hover { background-color: darkred; }
            .problem-button {
                background-color: #0078d7; color: white; font-size: 20pt; border-radius: 2px; padding: 50px; }
            .problem-button:hover {
                background-color: #005fa3; }
            QHeaderView::section {
                background-color: #52adf7;
                color: white;
            }
        """)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setSpacing(10)

        # Create the header label
        self.header_label = QLabel("Choose a Problem to Solve", self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)

        # Create the problem selection buttons
        self.problem_selection_layout = QHBoxLayout()
        self.production_planning_button = QPushButton("Production Planning", self)
        self.production_planning_button.setObjectName("production_planning")
        self.production_planning_button.setFixedSize(400, 200)
        self.production_planning_button.setProperty("class", "problem-button")

        self.knapsack_button = QPushButton("Knapsack", self)
        self.knapsack_button.setObjectName("knapsack")
        self.knapsack_button.setFixedSize(400, 200)
        self.knapsack_button.setProperty("class", "problem-button")

        self.problem_selection_layout.addWidget(self.production_planning_button)
        self.problem_selection_layout.addWidget(self.knapsack_button)
        self.layout.addLayout(self.problem_selection_layout)

        # Connect buttons to their respective methods
        self.production_planning_button.clicked.connect(lambda: self.display_selected_problem(1))
        self.knapsack_button.clicked.connect(lambda: self.display_selected_problem(2))

        # Common Back Button (used across different layouts)
        self.back_button = QPushButton("Back", self)
        self.back_button.clicked.connect(self.go_back_to_selection)
        self.layout.addWidget(self.back_button)
        self.back_button.hide()

        # Initialize problem layouts
        self.pp_layout = None
        self.kp_layout = None

    def go_back_to_selection(self):
        self.clear_current_layout()
        self.header_label.show()
        self.production_planning_button.show()
        self.knapsack_button.show()
        self.back_button.hide()

    def clear_current_layout(self):
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            widget = item.widget()
            if widget and widget != self.back_button:
                widget.hide()
            elif widget:
                self.layout.removeWidget(widget)
            else:
                layout = item.layout()
                if layout:
                    self.clear_layout(layout)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget and widget != self.back_button:
                widget.hide()
            elif widget:
                layout.removeWidget(widget)
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self.clear_layout(sub_layout)

    def display_selected_problem(self, index):
        self.clear_current_layout()
        if index == 1:
            self.init_production_planning_layout()
        elif index == 2:
            self.init_knapsack_layout()
        self.back_button.show()

    def init_production_planning_layout(self):
        if self.pp_layout is None:
            self.pp_layout = QVBoxLayout()
            self.constraints_pp = {}
            self.table_widget_pp = QTableWidget()
            self.table_widget_pp.setAlternatingRowColors(True)
            self.table_widget_pp.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table_widget_pp.setColumnCount(2)
            self.table_widget_pp.setHorizontalHeaderLabels(["Name", "Profit"])
            self.pp_layout.addWidget(self.table_widget_pp)


            self.add_column_button_pp = QPushButton("Add Constraint", self)
            self.add_column_button_pp.clicked.connect(lambda: self.add_new_column(layout=1))
            self.pp_layout.addWidget(self.add_column_button_pp)

            self.remove_column_button_pp = QPushButton("Remove Constraint", self)
            self.remove_column_button_pp.clicked.connect(lambda: self.remove_constraint_popup(layout=1))
            self.pp_layout.addWidget(self.remove_column_button_pp)


            self.max_value_inputs_pp = {}
            self.add_item_button_pp = QPushButton("Add Item", self)
            self.add_item_button_pp.clicked.connect(lambda: self.add_item_row(layout=1))
            self.pp_layout.addWidget(self.add_item_button_pp)
            self.solve_pp_btn = QPushButton('Solve Production Problem', self)
            self.solve_pp_btn.setObjectName("solve-button")
            self.solve_pp_btn.setProperty("class", "solve-button")
            self.solve_pp_btn.clicked.connect(self.solve_production_planning)
            self.pp_layout.addWidget(self.solve_pp_btn)
            self.pp_results_label = QTextEdit()
            self.pp_results_label.setReadOnly(True)
            self.pp_layout.addWidget(self.pp_results_label)
            self.pp_layout.addWidget(self.back_button)
        self.add_item_row(layout=1)
        self.show_layout(self.pp_layout)

    def init_knapsack_layout(self):
        if self.kp_layout is None:
            self.kp_layout = QVBoxLayout()
            self.constraints_kp = {}
            self.table_widget = QTableWidget()
            self.table_widget.setAlternatingRowColors(True)
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table_widget.setColumnCount(1)
            self.table_widget.setHorizontalHeaderLabels(["Value"])
            self.kp_layout.addWidget(self.table_widget)

            self.add_column_button = QPushButton("Add Constraint", self)
            self.add_column_button.clicked.connect(lambda: self.add_new_column(layout=2))
            self.kp_layout.addWidget(self.add_column_button)

            self.remove_column_button = QPushButton("Remove Constraint", self)
            self.remove_column_button.clicked.connect(lambda: self.remove_constraint_popup(layout=2))
            self.kp_layout.addWidget(self.remove_column_button)

            self.max_value_inputs = {}
            self.add_item_button = QPushButton("Add Item", self)
            self.add_item_button.clicked.connect(lambda: self.add_item_row(layout=2))
            self.kp_layout.addWidget(self.add_item_button)
            
            self.solve_kp_btn = QPushButton('Solve Knapsack Problem', self)
            self.solve_kp_btn.setObjectName("solve-button")
            self.solve_kp_btn.setProperty("class", "solve-button")
            self.solve_kp_btn.clicked.connect(self.solve_knapsack)
            self.kp_layout.addWidget(self.solve_kp_btn)
            self.kp_results_label = QTextEdit()
            self.kp_results_label.setReadOnly(True)
            self.kp_layout.addWidget(self.kp_results_label)
            self.kp_layout.addWidget(self.back_button)
        self.add_item_row(layout=2)
        self.show_layout(self.kp_layout)

    def show_layout(self, layout):
        if layout.parent() is not None:
            layout.parent().layout().removeItem(layout)
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                widget.show()
            else:
                sub_layout = item.layout()
                if sub_layout:
                    self.show_layout(sub_layout)
        self.layout.addLayout(layout)

    def add_new_column(self, layout):
        self.insertedColumns += 1
        if layout == 2:
            use_layout = self.kp_layout
            table = self.table_widget
            max_values = self.max_value_inputs
            constraints = self.constraints_kp
        else:
            use_layout = self.pp_layout
            table = self.table_widget_pp
            max_values = self.max_value_inputs_pp
            constraints = self.constraints_pp

        column_name, ok = QInputDialog.getText(self, "New Constraint", "Enter constraint name:")
        if ok and column_name:
            current_column_count = table.columnCount()
            table.setColumnCount(current_column_count + 1)
            table.setHorizontalHeaderItem(current_column_count, QTableWidgetItem(column_name))
            for row in range(table.rowCount()):
                table.setItem(row, current_column_count, QTableWidgetItem(""))
            label = QLabel(f"Available {column_name}", self)
            line_edit = QLineEdit(self)
            print(len(use_layout) - 1)
            use_layout.insertWidget(len(use_layout) - 1, label)
            print(len(use_layout) - 1)
            use_layout.insertWidget(len(use_layout) - 1, line_edit)
            constraints[column_name] = (len(use_layout) - 1, self.insertedColumns)
            max_values[column_name] = line_edit

    def remove_constraint_popup(self, layout):
        if layout == 2:
            constraints = self.constraints_kp
        else:
            constraints = self.constraints_pp
        # Create popup window
        self.popup = QWidget()  # Assign to self.popup
        popup_layout = QVBoxLayout(self.popup)

        # Label for column selection
        label = QLabel("Select Column to Remove:")
        popup_layout.addWidget(label)

        # Populate combobox with column names
        column_names = list(constraints.keys())
        combobox = QComboBox(self.popup)
        combobox.addItems(column_names)

        # Button to confirm removal
        confirm_button = QPushButton("Remove")
        confirm_button.clicked.connect(lambda: self.remove_constraint(layout=layout, column_name=combobox.currentText()))
        popup_layout.addWidget(confirm_button)

        # Button to cancel
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.popup.close)
        popup_layout.addWidget(cancel_button)

        # Display popup window
        self.popup.setWindowTitle("Remove Constraint")
        self.popup.show()

    def remove_constraint(self, layout, column_name):
        if layout == 2:
            use_layout = self.kp_layout
            table = self.table_widget
            max_values = self.max_value_inputs
            constraints = self.constraints_kp
            offset = 0
        else:
            use_layout = self.pp_layout
            table = self.table_widget_pp
            max_values = self.max_value_inputs_pp
            constraints = self.constraints_pp
            offset = 1

        print(column_name, constraints[column_name])
        toRemove1 = use_layout.itemAt(constraints[column_name][0]-1+offset)
        toRemove2 = use_layout.itemAt(constraints[column_name][0]-2+offset)

        table.removeColumn(constraints[column_name][1+offset])
        use_layout.removeWidget(toRemove1.widget())
        use_layout.removeWidget(toRemove2.widget())

        constraints.pop(column_name)
        max_values.pop(column_name)

    def add_item_row(self, layout):
        if layout == 2:
            num_rows = self.table_widget.rowCount()
            self.table_widget.insertRow(num_rows)
            item = QTableWidgetItem("")
            self.table_widget.setItem(num_rows, 0, item)
        else:
            num_rows = self.table_widget_pp.rowCount()
            self.table_widget_pp.insertRow(num_rows)
            item = QTableWidgetItem("")
            self.table_widget_pp.setItem(num_rows, 0, item)

    def solve_knapsack(self):
        try:
            item_count = self.table_widget.rowCount()
            values = [self.table_widget.item(row, 0) for row in range(item_count)]
            if any(value == None for value in values):
                raise ValueError("all item values must be filled")

            values = [self.table_widget.item(row, 0).text() for row in range(item_count)]
            if any(not value.isdigit() for value in values):
                raise ValueError("Item values must be numbers")
            values = [float(self.table_widget.item(row, 0).text()) for row in range(item_count)]
            if any(value <= 0 for value in values):
                raise ValueError("Items must have strictly positive values")
            
            constraint_values = {}
            for col, max_value_input in enumerate(self.max_value_inputs.values(), start=1):
                constraint_name = self.table_widget.horizontalHeaderItem(col).text()
                if not max_value_input.text().isdigit():
                    raise ValueError("Max value for constraint ", constraint_name, " must be a number")
                max_value = float(max_value_input.text())
                if max_value <= 0:
                    raise ValueError("Max value ", constraint_name, " must be a strictly positive number")
                
                cvalues = [self.table_widget.item(row, col) for row in range(item_count)]
                if any(value == None for value in cvalues):
                    raise ValueError("all constraint values must be filled")
                cvalues = [self.table_widget.item(row, col).text() for row in range(item_count)]
                if any(not value.isdigit() for value in cvalues):
                    raise ValueError("item ", constraint_name, " must be a number")
                cvalues = [float(self.table_widget.item(row, col).text()) for row in range(item_count)]
                if any(value < 0 for value in cvalues):
                    raise ValueError("item ", constraint_name, " value must be a positive number")
                
                constraint_values[constraint_name] = {
                    'values': [float(self.table_widget.item(row, col).text()) for row in range(item_count)],
                    'max': max_value
                }
            result = solve_knapsack(values, constraint_values)
            if result:
                selected_items, total_value, time = result
                selected_items_text = ', '.join([f"Item {index + 1}" for index in selected_items])
                result_text = f"Selected items: {selected_items_text}\nTotal value: {total_value}\nTime taken: {time} seconds."
                self.kp_results_label.setText(result_text)
            else:
                self.kp_results_label.setText("No solution found.")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

    def solve_production_planning(self):
        try:
            item_count = self.table_widget_pp.rowCount()
            values = [self.table_widget_pp.item(row, 1) for row in range(item_count)]
            if any(value == None for value in values):
                raise ValueError("Please fill all values")
            

            values = [self.table_widget_pp.item(row, 1).text() for row in range(item_count)]
            if any(value == "" for value in values):
                raise ValueError("Please fill all values")
            
            if any(not value.isdigit() for value in values):
                raise ValueError("Item values must be numbers")
            
            values = [float(self.table_widget_pp.item(row, 1).text()) for row in range(item_count)]
            
            if any(value <= 0 for value in values):
                raise ValueError("Items must have strictly positive values")
            
            names = [self.table_widget_pp.item(row, 0).text() for row in range(item_count)]

            if any(name == "" for name in names):
                raise ValueError("Items must have a non empty name")
            
            products = [{'name': names[i], 'profit': values[i]} for i in range(item_count)]

            constraints = {}
            for col, max_value_input in enumerate(self.max_value_inputs_pp.values(), start=2):
                constraint_name = self.table_widget_pp.horizontalHeaderItem(col).text()
                if not max_value_input.text().isdigit():
                    raise ValueError("Max value for constraint ", constraint_name, " must be a number")
                
                max_value = float(max_value_input.text())
                if max_value <= 0:
                    raise ValueError("Max value ", constraint_name, " must be a strictly positive number")
                
                cvalues = [self.table_widget_pp.item(row, col) for row in range(item_count)]
                if any(value == None for value in cvalues):
                    raise ValueError("all constraint values must be filled")
                
                cvalues = [self.table_widget_pp.item(row, col).text() for row in range(item_count)]
                if any(not value.isdigit() for value in cvalues):
                    raise ValueError(constraint_name, " for all items must be a number")
                cvalues = [float(self.table_widget_pp.item(row, col).text()) for row in range(item_count)]
                if any(value < 0 for value in cvalues):
                    raise ValueError(constraint_name, " for all items must be a positive number")
                
                constraints[constraint_name] = {
                    'values': [float(self.table_widget_pp.item(row, col).text()) for row in range(item_count)],
                    'max': max_value
                }

            result = solve_production(products, constraints)
            if result:
                production_levels = result['Production Levels']
                total_profit = result['Total Profit']
                result_text = "Production Levels:\n" + "\n".join([f"{product}: {level}" for product, level in production_levels.items()])
                result_text += f"\nTotal Profit: {total_profit}"
                self.pp_results_label.setText(result_text)
            else:
                self.pp_results_label.setText("No solution found.")
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OptimizationApp()
    ex.show()
    sys.exit(app.exec_())


