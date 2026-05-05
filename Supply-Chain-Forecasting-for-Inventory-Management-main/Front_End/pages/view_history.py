import pandas as pd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QDateEdit
)
from PyQt6.QtCore import QDate, Qt


class ViewHistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.data = pd.read_csv("Data\\Data_Set.csv")

        # Layout setup
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        # Date input with format matching CSV (dd-MM-yyyy)
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setStyleSheet("padding: 6px; font-size: 14px;")

        # Store ID and Product ID inputs
        self.store_id_input = QLineEdit()
        self.store_id_input.setPlaceholderText("Enter Store ID (e.g., S001)")
        self.store_id_input.setStyleSheet("padding: 6px; font-size: 14px;")

        self.product_id_input = QLineEdit()
        self.product_id_input.setPlaceholderText("Enter Product ID (e.g., P0001)")
        self.product_id_input.setStyleSheet("padding: 6px; font-size: 14px;")

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_data)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #8E8EA3;
                color: white;
                padding: 6px 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
        """)

        # Add widgets to search layout
        search_layout.addWidget(self.date_input)
        search_layout.addWidget(self.store_id_input)
        search_layout.addWidget(self.product_id_input)
        search_layout.addWidget(self.search_button)

        # Table to display data
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.data.columns))
        self.table.setHorizontalHeaderLabels(self.data.columns.tolist())
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #A79B9B;
                color: #333;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px; 
                padding: 10px;
                alternate-background-color: #e6f2ff;
                font-size: 13px;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #8E8EA3;
                color: white;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #ccc;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
                                 
            }
        """)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSortingEnabled(True)

        # Add to main layout
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    def search_data(self):
        date_input = self.date_input.date().toString("dd-MM-yyyy")
        store_input = self.store_id_input.text().strip()
        product_input = self.product_id_input.text().strip()

        df = self.data.copy()

        if date_input:
            df = df[df['Date'].astype(str) == date_input]

        if store_input:
            df = df[df['Store ID'].astype(str).str.upper() == store_input.upper()]

        if product_input:
            df = df[df['Product ID'].astype(str).str.upper() == product_input.upper()]

        if df.empty:
            QMessageBox.information(self, "No Results", "No matching records found.")
            self.table.setRowCount(0)
            return

        self.table.setRowCount(len(df))
        for row_idx, (_, row) in enumerate(df.iterrows()):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
