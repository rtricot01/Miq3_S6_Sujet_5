import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton

from reservation_calendrier import Calendrier
from reservation_prix import Prix
from reservation_personne import NombrePersonne
from reservation_services import Services

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from Controleur import classe_objet

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

        bouton_valider = QPushButton("Valider")
        bouton_valider.clicked.connect(self.action_bouton)

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
        layout_global.addWidget(bouton_valider)

    def action_bouton (self) :
        date_debut = self.calendrier.date_debut.text()
        date_fin = self.calendrier.date_fin.text()
        min_people = self.personne.textBox_nbr_adulte.text() + self.personne.textBox_nbr_enfant.text()
        fumeur = self.services.checkBox_fumeur.isChecked()
        animaux_toleres = self.services.checkBox_animaux.isChecked()
        climatisation = self.services.checkBox_climatisation.isChecked()
        prix_min = self.prix.slider_prix_minimal.value()
        prix_max = self.prix.slider_prix_maximal.value()

        chambres_disponibles = classe_objet.recuperer_chambre_libre(date_debut,date_fin, min_people, fumeur, animaux_toleres, climatisation, prix_min, prix_max)
        print(chambres_disponibles)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = FenetreReservation()
    myWindow.show()
    sys.exit(app.exec())
