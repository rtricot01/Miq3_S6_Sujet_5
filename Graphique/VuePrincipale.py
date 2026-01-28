import sys
from datetime import date

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget,  QLabel, QPushButton


class MyWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Some widgets")
        self.setWindowIcon(QIcon("icons/file.png"))
        self.resize(570, 600)

        # Le type QWidget représente un conteneur de widgets (et il est lui-même un widget).
        # On crée une instance que l'on va mettre au centre de la fenêtre.
        centralArea = QWidget()
        # On injecte ce widget en tant que zone centrale.
        self.setCentralWidget(centralArea)


        label = QLabel("Bienvenue !", centralArea)
        label.setGeometry(250, 10, 270, 30)

        label = QLabel("Cliquez sur le bouton correspondant à votre besoin", centralArea)
        label.setGeometry(130, 30, 270, 30)



        button = QPushButton("Créer une chambre", centralArea)
        button.setGeometry(10, 70, 270, 60)
        # On connecte le signal clicked exposé par le bouton au slot dateSelected.
        button.clicked.connect(self.buttonClicked)

        button = QPushButton("Voir les réservations", centralArea)
        button.setGeometry(290, 70, 270, 60)
        # On connecte le signal clicked exposé par le bouton au slot dateSelected.
        button.clicked.connect(self.buttonClicked)

        button = QPushButton("Prendre une réservation", centralArea)
        button.setGeometry(10, 140, 270, 60)
        # On connecte le signal clicked exposé par le bouton au slot dateSelected.
        button.clicked.connect(self.buttonClicked)

        button = QPushButton("Voir les chambres", centralArea)
        button.setGeometry(290, 140, 270, 60)
        # On connecte le signal clicked exposé par le bouton au slot dateSelected.
        button.clicked.connect(self.buttonClicked)

  

    @Slot()
    def buttonClicked(self):
        btn = self.sender()
        print(f"Button <{btn.text()}> clicked")

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec())