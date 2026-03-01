import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QMessageBox, QListWidgetItem
)
from PyQt6.QtCore import Qt, QSize
from task_manager import load_tasks, add_task, complete_task, delete_task

class TaskFlowGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TaskFlow")
        self.setMinimumSize(400, 550)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 15px;
                background-color: #4285f4;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #357ae8;
            }
            QPushButton#deleteButton {
                background-color: #db4437;
            }
            QPushButton#deleteButton:hover {
                background-color: #c53929;
            }
            QPushButton#completeButton {
                background-color: #0f9d58;
            }
            QPushButton#completeButton:hover {
                background-color: #0b8043;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                font-size: 14px;
                outline: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e8f0fe;
                color: #1967d2;
            }
        """)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Input Area
        input_layout = QHBoxLayout()
        self.task_entry = QLineEdit()
        self.task_entry.setPlaceholderText("Enter a new task...")
        self.task_entry.returnPressed.connect(self.add_task_gui)

        add_button = QPushButton("Add Task")
        add_button.clicked.connect(self.add_task_gui)

        input_layout.addWidget(self.task_entry)
        input_layout.addWidget(add_button)
        main_layout.addLayout(input_layout)

        # Task List
        self.task_list_widget = QListWidget()
        main_layout.addWidget(self.task_list_widget)

        # Action Buttons
        button_layout = QHBoxLayout()

        self.complete_button = QPushButton("Complete")
        self.complete_button.setObjectName("completeButton")
        self.complete_button.clicked.connect(self.complete_task_gui)

        self.delete_button = QPushButton("Delete")
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_task_gui)

        button_layout.addWidget(self.complete_button)
        button_layout.addWidget(self.delete_button)
        main_layout.addLayout(button_layout)

        self.refresh_list()

    def refresh_list(self):
        self.task_list_widget.clear()
        tasks = load_tasks()
        for task in tasks:
            status = "✓ " if task["completed"] else "○ "
            item_text = f"{status} {task['title']}"
            item = QListWidgetItem(item_text)
            if task["completed"]:
                item.setForeground(Qt.GlobalColor.gray)
            self.task_list_widget.addItem(item)

    def add_task_gui(self):
        title = self.task_entry.text().strip()
        if title:
            add_task(title)
            self.task_entry.clear()
            self.refresh_list()
        else:
            QMessageBox.warning(self, "Warning", "You must enter a task.")

    def complete_task_gui(self):
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            index = current_row + 1
            if complete_task(index):
                self.refresh_list()
        else:
            QMessageBox.warning(self, "Warning", "Select a task to complete.")

    def delete_task_gui(self):
        current_row = self.task_list_widget.currentRow()
        if current_row >= 0:
            index = current_row + 1
            if delete_task(index):
                self.refresh_list()
        else:
            QMessageBox.warning(self, "Warning", "Select a task to delete.")

def main():
    app = QApplication(sys.argv)
    window = TaskFlowGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
