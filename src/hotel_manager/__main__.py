import sys
from PySide6.QtWidgets import QApplication
from src.hotel_manager.graphique.vue_principale import VuePrincipale
from src.hotel_manager.utils.logging_config import setup_logging

def main():
    setup_logging()
    app = QApplication(sys.argv)
    main_win = VuePrincipale()
    main_win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()