import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

from reservation_calendrier import Calendrier
from reservation_prix import Prix
from reservation_personne import NombrePersonne


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

        layout_global = QHBoxLayout(fenetre_principale)

        self.calendrier = Calendrier()
        self.prix = Prix(self.PRIX_MAXIMAL)
        self.personne = NombrePersonne()
        
        layout_global.setSpacing(40)
        layout_global.addWidget(self.calendrier)
        layout_global.addWidget(self.prix)
        layout_global.addWidget(self.personne)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = FenetreReservation()
    myWindow.show()
    sys.exit(app.exec())
