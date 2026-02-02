from PySide6.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QFrame, QCheckBox)
from PySide6.QtCore import Qt, QSize, Signal, Slot
from PySide6.QtGui import QIcon
import sys

class VueReservationTotal(QMainWindow):
    changeItem = Signal(list)

    def __init__(self, items=None, parent=None):
        super(VueReservationTotal, self).__init__(parent)
        self.setWindowTitle("Application de gestion de reservation")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(310, 300)

        central_area = QWidget()
        self.setCentralWidget(central_area)
        main_layout = QVBoxLayout(central_area)

        self.label = QLabel("Liste des Réservations")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px;")
        main_layout.addWidget(self.label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        main_layout.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll_layout = QVBoxLayout(self.container)
        self.scroll.setWidget(self.container)

        self.listItem = items if items else [0] * 20
        self.listState = [False] * len(self.listItem)
        self.itemChk = []

        self.initUI()
        
    def initUI(self): 
        for i, s in enumerate(self.listItem):
            chk = QCheckBox(f"Objet {i}")
            chk.setChecked(False)
            chk.stateChanged.connect(self.changeChk)
            self.itemChk.append(chk)
            self.scroll_layout.addWidget(chk)
    
    def changeChk(self, state):
        sender = self.sender()
        is_checked = state > 0
        print(f"{sender.text()} : {is_checked}")
        
        for i, chk in enumerate(self.itemChk):
            if chk == sender:
                self.listState[i] = is_checked
        
        self.changeItem.emit(self.listState)

def main():
    app = QApplication(sys.argv)
    window = VueReservationTotal()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
