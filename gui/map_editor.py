# gui/map_editor.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QLabel, QComboBox
)
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPen, QBrush, QColor, QFont, QFontDatabase, QPixmap
import json
import os

class MapEditor(QWidget):
    def __init__(self, quest_id=None):
        super().__init__()
        self.quest_id = quest_id or 0
        self.items = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🗺️ Quest Map Editor")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Location type selector
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Город 🟢", "Логово 🔴", "Таверна 🟡"])
        layout.addWidget(self.type_combo)

        # Buttons
        add_btn = QPushButton("✚ Добавить локацию")
        add_btn.clicked.connect(self.add_location)
        layout.addWidget(add_btn)

        erase_btn = QPushButton("🧹 Стереть последнее")
        erase_btn.clicked.connect(self.erase_last)
        layout.addWidget(erase_btn)

        save_img_btn = QPushButton("📷 Сохранить как PNG")
        save_img_btn.clicked.connect(self.save_as_image)
        layout.addWidget(save_img_btn)

        # Graphics view
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 600)
        self.scene.setBackgroundBrush(QBrush(QColor("#f4e4bc")))  # Parchment

        self.view = QGraphicsView(self.scene)
        self.view.setFixedSize(820, 620)
        self.view.setRenderHint(self.view.renderHint().Antialiasing)

        layout.addWidget(self.view)
        self.setLayout(layout)

        # Load custom font if available
        font_path = "assets/fonts/UncialAntiqua-Regular.ttf"
        if os.path.exists(font_path):
            QFontDatabase.addApplicationFont(font_path)

    def add_location(self):
        x, y = 400 + len(self.items) * 50, 300
        loc_type = self.type_combo.currentText()
        color_map = {"Город 🟢": Qt.GlobalColor.green, "Логово 🔴": Qt.GlobalColor.red, "Таверна 🟡": Qt.GlobalColor.yellow}
        color = color_map.get(loc_type.split()[0], Qt.GlobalColor.gray)

        # Marker
        ellipse = self.scene.addEllipse(x - 15, y - 15, 30, 30, QPen(Qt.GlobalColor.black), QBrush(color))
        self.items.append(ellipse)

        # Label
        label = self.scene.addText(loc_type.split()[0], QFont("Uncial Antiqua", 10))
        label.setDefaultTextColor(Qt.GlobalColor.black)
        label.setPos(x - 20, y + 20)
        self.items.append(label)

    def erase_last(self):
        if self.items:
            item = self.items.pop()
            self.scene.removeItem(item)

    def save_as_image(self):
        """Save scene as PNG linked to quest."""
        pixmap = QPixmap(int(self.scene.width()), int(self.scene.height()))
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = self.scene.render
        painter = self.scene.render
        # Use QGraphicsView to render
        image_path = f"maps/map_quest_{self.quest_id}.png"
        os.makedirs("maps", exist_ok=True)
        self.scene.setSceneRect(QRectF(0, 0, 800, 600))
        pixmap = QPixmap(800, 600)
        pixmap.fill(QColor("#f4e4bc"))
        painter = pixmap
        from PyQt6.QtGui import QPainter
        p = QPainter(pixmap)
        self.scene.render(p)
        p.end()
        pixmap.save(image_path, "PNG")
        print(f"Map saved: {image_path}")