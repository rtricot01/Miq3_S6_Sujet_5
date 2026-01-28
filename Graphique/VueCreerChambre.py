import sys
from datetime import date

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QCalendarWidget, QLabel, \
                              QPushButton, QCheckBox, QSpinBox, QLCDNumber, QLineEdit, \
                              QSlider, QProgressBar


class MyWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Application de gestion de reservation")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(310, 300)

        centralArea = QWidget()
        self.setCentralWidget(centralArea)


        label = QLabel("Formulaire de création de chambre", centralArea)
        label.setGeometry(20, 10, 270, 20)

        label = QLabel("Nombre de chambre", centralArea)
        label.setGeometry(20, 30, 270, 20)
        textBox = QLineEdit("Ex : 3", centralArea)
        textBox.setGeometry(20, 50, 270, 30)

        label = QLabel("Prix de la nuit en Euro", centralArea)
        label.setGeometry(20, 90, 270, 20)
        textBox = QLineEdit("Ex : 200€", centralArea)
        textBox.setGeometry(20, 110, 270, 30)

        label = QLabel("Superficie en m² :", centralArea)
        label.setGeometry(20, 150, 270, 20)
        textBox = QLineEdit("Ex : 30m²", centralArea)
        textBox.setGeometry(20, 170, 270, 30)


       
    @Slot()
    def buttonClicked(self):
        btn = self.sender()
        print(f"Button <{btn.text()}> clicked")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec())