import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from reservation_calendrier import Calendrier
from reservation_prix import Prix
from reservation_personne import NombrePersonne
from reservation_services import Services


class FenetreReservation (QMainWindow):

    PRIX_MAXIMAL = 500.0

    def __init__(self,parent=None):
        super(FenetreReservation, self).__init__(parent)

        self.setWindowTitle("Réservation d'une Chambre")
        self.setWindowIcon(QIcon("icone_chambre.png"))
        self.showMaximized()
        fenetre_principale = QWidget()
        fenetre_principale.setStyleSheet("background: #C6B7D1")
        self.setCentralWidget(fenetre_principale)

        layout_global = QVBoxLayout (fenetre_principale)
        layout_top = QHBoxLayout()


        self.calendrier = Calendrier()
        self.prix = Prix(self.PRIX_MAXIMAL)
        self.personne = NombrePersonne()
        self.services = Services()

        layout_global.addWidget(self.services)
        
        layout_top.setSpacing(40)
        layout_top.addWidget(self.calendrier)
        layout_top.addWidget(self.prix)
        layout_top.addWidget(self.personne)

        layout_global.addLayout(layout_top)
        layout_global.setSpacing(20)
        layout_global.addWidget(self.services)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = FenetreReservation()
    myWindow.show()
    sys.exit(app.exec())
