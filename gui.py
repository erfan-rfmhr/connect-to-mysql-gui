from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QHeaderView

from db import Database


class App(QMainWindow):
    def __init__(self, host, user, password, database):
        super().__init__()

        self.db = Database(host, user, password, database)

        # Create main widget and layout
        widget = QWidget()
        layout = QGridLayout()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Create input fields
        self.table_input = QLineEdit()
        self.fields_input = QLineEdit()
        self.values_input = QLineEdit()
        self.where_input = QLineEdit()
        self.limit_input = QLineEdit()
        self.table_widget = QTableWidget()

        # Add input labels and fields to layout
        layout.addWidget(QLabel("Table:"), 0, 0)
        layout.addWidget(self.table_input, 0, 1)
        layout.addWidget(QLabel("Fields:"), 1, 0)
        layout.addWidget(self.fields_input, 1, 1)
        layout.addWidget(QLabel("Values:"), 2, 0)
        layout.addWidget(self.values_input, 2, 1)
        layout.addWidget(QLabel("Where:"), 3, 0)
        layout.addWidget(self.where_input, 3, 1)
        layout.addWidget(QLabel("Limit:"), 4, 0)
        layout.addWidget(self.limit_input, 4, 1)
        layout.addWidget(self.table_widget, 7, 0, 1, 2)

        # Create buttons and connect them to functions
        read_button = QPushButton("Read")
        read_button.clicked.connect(self.read_data)
        layout.addWidget(read_button, 5, 0)

        insert_button = QPushButton("Insert")
        insert_button.clicked.connect(self.insert_data)
        layout.addWidget(insert_button, 5, 1)

        update_button = QPushButton("Update")
        update_button.clicked.connect(self.update_data)
        layout.addWidget(update_button, 6, 0)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_data)
        layout.addWidget(delete_button, 6, 1)

    def read_data(self):
        pass
        table = self.table_input.text()
        fields = self.fields_input.text().split(",")
        if fields[0] == '':
            fields = '*'
        values = self.values_input.text().split(",")
        if values[0] == '':
            values = tuple()
        where = self.where_input.text() if self.where_input.text() != '' else None
        limit = int(self.limit_input.text()) if self.limit_input.text() else None
        data = self.db.get(table, fields, where, limit, values)

        self.table_widget.clearContents()
        # Row count
        row_counts = len(data)
        self.table_widget.setRowCount(row_counts)

        # Column count
        if fields == '*':
            fields = self.db.get_table_fields(table)
        col_counts = len(fields)
        self.table_widget.setColumnCount(col_counts)

        # display fields
        for col, field_name in zip(range(col_counts), fields):
            self.table_widget.setItem(0, col, QTableWidgetItem(field_name))

        for row in range(1, row_counts + 1):
            for col in range(col_counts):
                self.table_widget.setItem(row, col, QTableWidgetItem(str(data[row-1][col])))

        # Table will fit the screen horizontally
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

    def insert_data(self):
        table = self.table_input.text()
        fields = tuple(self.fields_input.text().split(","))
        values = tuple(self.values_input.text().split(","))
        try:
            self.db.insert(table, fields, values)
        except Exception as e:
            print(e)

    def update_data(self):
        table = self.table_input.text()
        fields = tuple(self.fields_input.text().split(","))
        values = tuple(self.values_input.text().split(","))
        where = self.where_input.text()

        self.db.update(table, fields, values, where)

    def delete_data(self):
        table = self.table_input.text()
        where = self.where_input.text()
        values = tuple(self.values_input.text().split(","))

        self.db.delete(table, where, values)
