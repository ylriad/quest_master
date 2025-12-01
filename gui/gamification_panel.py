# gui/gamification_panel.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl, Qt
from core.gamification import GamificationEngine
import sys
import os

class GamificationPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.engine = GamificationEngine()
        self.init_ui()
        self.update_display()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title = QLabel("🏅 Adventure Progress")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Level %v — %p% to next")

        layout.addWidget(self.title)
        layout.addWidget(self.level_label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def update_display(self):
        status = self.engine.get_status()
        self.level_label.setText(f"Level {status['level']} | {status['xp']} / {status['xp_to_next']} XP")
        self.progress_bar.setRange(0, status["xp_to_next"])
        self.progress_bar.setValue(status["xp"])

    def award_xp(self, amount: int):
        """Call this when user completes a quest, etc."""
        self.engine.add_xp(amount)
        self.update_display()

        # Optional: Play level-up sound if leveled
        if self.engine.get_status()["xp"] == 0 and self.engine.level > 1:
            self._play_level_up_sound()

    def _play_level_up_sound(self):
        # Only play if sound file exists
        sound_path = self._resource_path("sounds/level_up.wav")
        if os.path.exists(sound_path):
            effect = QSoundEffect()
            effect.setSource(QUrl.fromLocalFile(sound_path))
            effect.setVolume(0.8)
            effect.play()

    def _resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and PyInstaller."""
        try:
            base_path = sys._MEIPASS  # PyInstaller temp folder
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, "..", relative_path)