# main.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget

from gui.quest_wizard import QuestWizard
from gui.map_editor import MapEditor
from gui.gamification_panel import GamificationPanel

class QuestMasterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛡️ Quest Master — RPG Quest Designer")
        self.setGeometry(100, 100, 800, 700)

        # Create widgets first
        self.quest_wizard = QuestWizard()
        self.map_editor = MapEditor()
        self.gamification_panel = GamificationPanel()

        # Central tab widget
        tabs = QTabWidget()
        tabs.addTab(self.quest_wizard, "📝 Quest Wizard")
        tabs.addTab(self.map_editor, "🗺️ Map Editor")
        tabs.addTab(self.gamification_panel, "🏅 Progress")

        self.setCentralWidget(tabs)

        # Optional: Demo XP award (remove later)
        self.gamification_panel.award_xp(30)

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Consistent look
    window = QuestMasterApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()