# gui/quest_wizard.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QTextEdit, QPushButton, QDateTimeEdit, QMessageBox, QSpinBox, QApplication
)
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtGui import QKeySequence, QShortcut
import sys
from core.database import QuestDatabase

class QuestWizard(QWidget):
    def __init__(self):
        super().__init__()
        self.db = QuestDatabase()
        self.init_ui()
        self.setup_shortcuts()
        self.update_desc_counter()  # Init counter

    def init_ui(self):
        layout = QVBoxLayout()

        # Title (max 50 chars)
        layout.addWidget(QLabel("Название квеста:"))
        self.title_input = QLineEdit()
        self.title_input.setMaxLength(50)
        self.title_input.textChanged.connect(self.validate)
        layout.addWidget(self.title_input)

        # Difficulty
        layout.addWidget(QLabel("Сложность:"))
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Легкий", "Средний", "Сложный", "Эпический"])
        layout.addWidget(self.difficulty_combo)

        # Reward (10–10000)
        layout.addWidget(QLabel("Награда (золото):"))
        self.reward_spin = QSpinBox()
        self.reward_spin.setRange(10, 10000)
        self.reward_spin.setValue(100)
        layout.addWidget(self.reward_spin)

        # Deadline
        layout.addWidget(QLabel("Дедлайн выполнения:"))
        self.deadline_edit = QDateTimeEdit()
        self.deadline_edit.setDateTime(QDateTime.currentDateTime().addDays(7))
        self.deadline_edit.setDisplayFormat("yyyy-MM-dd HH:mm")
        layout.addWidget(self.deadline_edit)

        # Description + live counter
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Описание (мин. 50 символов):"))
        self.desc_counter = QLabel("0")
        desc_layout.addWidget(self.desc_counter)
        layout.addLayout(desc_layout)

        self.desc_edit = QTextEdit()
        self.desc_edit.textChanged.connect(self.update_desc_counter)
        layout.addWidget(self.desc_edit)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Создать квест")
        self.save_btn.clicked.connect(self.save_quest)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def setup_shortcuts(self):
        # Ctrl+Enter to save
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        shortcut.activated.connect(self.save_quest)

    def update_desc_counter(self):
        text = self.desc_edit.toPlainText()
        self.desc_counter.setText(str(len(text)))

    def validate(self):
        title_ok = len(self.title_input.text().strip()) > 0
        desc_ok = len(self.desc_edit.toPlainText()) >= 50

        # Reset styles
        self.title_input.setStyleSheet("")
        self.desc_edit.setStyleSheet("")

        # Apply red border if invalid
        if not title_ok:
            self.title_input.setStyleSheet("border: 2px solid red;")
        if not desc_ok:
            self.desc_edit.setStyleSheet("border: 2px solid red;")

        return title_ok and desc_ok

    def save_quest(self):
        if not self.validate():
            QMessageBox.warning(self, "Ошибка валидации", "Заполните название и описание (мин. 50 символов).")
            return

        quest_id = self.db.add_quest(
            title=self.title_input.text().strip(),
            description=self.desc_edit.toPlainText(),
            difficulty=self.difficulty_combo.currentText(),
            deadline=self.deadline_edit.dateTime().toString("yyyy-MM-dd HH:mm:ss"),
            reward=self.reward_spin.value()
        )
        QMessageBox.information(self, "Успех", f"Квест создан! ID: {quest_id}")
        # Award XP via signal later (connect in main.py)
        self.quest_created.emit(quest_id)

    # Signal for XP system (optional but clean)
    from PyQt6.QtCore import pyqtSignal
    quest_created = pyqtSignal(int)