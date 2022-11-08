#!/usr/bin/env python3
"""Main window class"""
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from database import DatabaseSelect
from .element_window import ElementPage


class Main(QMainWindow):
    """Create perodic table window"""
    def __init__(self, config: dict):
        super().__init__()
        self.setGeometry(0, 0, 1280, 740)
        self.setWindowTitle("Periodic table of elements")
        self.database = DatabaseSelect(config)
        self.widgets = []
        self.buttons = []
        self.init_ui()

    def init_ui(self):
        """Set up the window"""
        for column in range(18):
            text = str(column + 1)
            self.btn = QLabel(text, self)
            # self.btn.resize(60, 60)
            self.btn.move(170 + 60 * column, 20)
            # self.btn.setEnabled(False)
            self.buttons += [self.btn]
        for row in range(7):
            text = str(row + 1)
            self.btn = QLabel(text, self)
            # self.btn.resize(60, 60)
            self.btn.move(110, 80 + 60 * row)
            # self.btn.setEnabled(False)
            self.buttons += [self.btn]
        basic_info = self.database.select_basic_info()
        table = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
                 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
        table += [[1 for _ in range(18)] for _ in range(2)]
        table += [[1 for _ in range(32)] for _ in range(2)]
        for row_index, row in enumerate(table):
            for column_index, column in enumerate(row):
                if not column:
                    continue
                number, name = basic_info.pop(0)
                btn_text = str(number) + " " + str(name)
                self.btn = QPushButton(btn_text, self)
                self.btn.resize(60, 60)
                match number:
                    case _ if 57 < number < 72:
                        self.btn.move(150 + 60 * column_index, 500)
                    case _ if 89 < number < 104:
                        self.btn.move(150 + 60 * column_index, 560)
                    case _:
                        if column_index > 17 or row_index in (5, 6) and column_index == 17:
                            column_index -= 14
                        self.btn.move(150 + 60 * column_index, 70 + 60 * row_index)
                self.btn.name = name
                self.btn.number = number
                self.btn.clicked.connect(self.open_element_page)
                self.buttons += [self.btn]
        self.database.close()

    def open_element_page(self):
        """Open element's page window when button is pressed"""
        sender = self.sender()
        widget = ElementPage(sender.name, sender.number)
        widget.show()
        self.widgets += [widget]
