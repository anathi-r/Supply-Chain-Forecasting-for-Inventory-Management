from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QDialog, QSizePolicy
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from random import randint, sample

class OverviewPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0f0f2d; color: white;")

        self.products = [f"P{i:04d}" for i in range(1, 21)]

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title = QLabel("TODAYS SALES PREDICTED")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        sales_layout = QHBoxLayout()
        sales_layout.setSpacing(15)

        self.S1 = randint(300, 350)
        self.S2 = randint(251, 310)
        self.S3 = randint(241, 330)
        self.S4 = randint(200, 300)
        self.S5 = randint(200, 300)

        sales_labels = {
            "Total Unit Sold": str(self.S1 + self.S2 + self.S3 + self.S4 + self.S5),
            "S001": str(self.S1),
            "S002": str(self.S2),
            "S003": str(self.S3),
            "S004": str(self.S4),
            "S005": str(self.S5),
        }

        for label, value in sales_labels.items():
            box = self.create_info_box(label, value)
            sales_layout.addWidget(box)

        main_layout.addLayout(sales_layout)

        chart_row = QHBoxLayout()
        chart_row.setSpacing(10)

        chart_row.addWidget(self.create_pie_chart())

        for store_data in [self.S1, self.S2, self.S3, self.S4, self.S5]:
            chart_row.addWidget(self.create_lollipop_chart(store_data))

        main_layout.addLayout(chart_row)

        main_layout.addWidget(self.create_chart_placeholder("Category-wise Units Sold", height=300))

        self.setLayout(main_layout)

    def create_info_box(self, title, value):
        frame = QFrame()
        frame.setStyleSheet("background-color: #1e1e3f; border-radius: 10px;")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        label_title = QLabel(title)
        label_title.setFont(QFont("Arial", 10))
        label_value = QLabel(value)
        label_value.setFont(QFont("Arial", 16, QFont.Weight.Bold))

        layout.addWidget(label_title)
        layout.addWidget(label_value)
        frame.setLayout(layout)
        return frame

    def split_into_unequal_parts(self, total, parts):
        cuts = sorted(sample(range(1, total), parts - 1))
        return [a - b for a, b in zip(cuts + [total], [0] + cuts)]

    def show_popup_with_chart(self, title, fig):
        popup = QDialog(self)
        popup.setWindowTitle(title)
        popup.setMinimumSize(800, 600)
        popup.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        canvas.updateGeometry()

        layout.addWidget(canvas)
        fig.tight_layout()

        popup.setLayout(layout)
        popup.exec()

    def create_pie_chart(self):
        frame = QFrame()
        frame.setMinimumHeight(200)
        layout = QVBoxLayout()

        fig = plt.Figure(figsize=(2.5, 2.5))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        frame.setLayout(layout)

        ax = fig.add_subplot(111)
        ax.pie([self.S1, self.S2, self.S3, self.S4, self.S5],
               labels=["S001", "S002", "S003", "S004", "S005"], autopct='%1.1f%%')
        ax.set_title("Total Sales")
        fig.tight_layout()

        canvas.mpl_connect("button_press_event", lambda event: self.show_popup_with_chart("Pie Chart", fig))

        return frame

    def create_lollipop_chart(self, store_total):
        frame = QFrame()
        frame.setMinimumHeight(200)
        layout = QVBoxLayout()

        fig = plt.Figure(figsize=(2.5, 2))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        frame.setLayout(layout)

        values = self.split_into_unequal_parts(store_total, 20)
        x = np.arange(20)
        ax = fig.add_subplot(111)
        ax.hlines(y=x, xmin=0, xmax=values, color="skyblue")
        ax.plot(values, x, "o")
        ax.set_yticks(x)
        ax.set_yticklabels(self.products, fontsize=6)
        ax.invert_yaxis()
        ax.set_title("Store Sales")
        fig.tight_layout()
        
        canvas.mpl_connect("button_press_event", lambda event: self.show_popup_with_chart("Store Sales", fig))

        if not hasattr(self, 'all_store_values'):
            self.all_store_values = []
        self.all_store_values.append(values)

        return frame

    def create_chart_placeholder(self, text, height=200):
        if text == "Category-wise Units Sold":
            return self.create_category_bar_chart(height)

        frame = QFrame()
        frame.setMinimumHeight(height)
        frame.setStyleSheet("background-color: #2c2c54; border-radius: 10px;")
        layout = QVBoxLayout()
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        frame.setLayout(layout)
        return frame

    def create_category_bar_chart(self, height=300):
        frame = QFrame()
        frame.setMinimumHeight(height)
        layout = QVBoxLayout()

        fig = plt.Figure(figsize=(9, 3.5))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        frame.setLayout(layout)

        ax = fig.add_subplot(111)
        ax.set_title("Category-wise Units Sold", fontsize=10)

        category_totals = [sum(product_sales) for product_sales in zip(*self.all_store_values)]

        x = np.arange(20)
        bars = ax.bar(x, category_totals, color='skyblue', edgecolor='blue', linewidth=0.5)

        for rect in bars:
            x_val = rect.get_x() + rect.get_width() / 2.0
            y_val = rect.get_height()
            ax.plot(x_val, y_val, marker="o", markersize=4, color="blue")

        ax.set_xticks(x)
        ax.set_xticklabels(self.products, rotation=90, fontsize=6)
        ax.set_facecolor("#2c2c54")
        fig.tight_layout()

        canvas.mpl_connect("button_press_event", lambda event: self.show_popup_with_chart("Category-wise Units Sold", fig))

        return frame
