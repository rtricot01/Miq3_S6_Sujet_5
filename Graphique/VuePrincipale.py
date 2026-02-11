import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton

from VueReservationTotal import VueReservationTotal 
from VueCreerChambre import VueCreerChambre
from VueChambreTot import VueChambreTot
#TODO rajouter les impport des vues PrendreRésa 


class VuePrincipale(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application de gestion de reservation")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(570, 600)

        
        centralArea = QWidget()
        self.setCentralWidget(centralArea)


        label = QLabel("Bienvenue !", centralArea)
        label.setGeometry(250, 10, 270, 30)

        label = QLabel("Cliquez sur le bouton correspondant à votre besoin", centralArea)
        label.setGeometry(130, 30, 270, 30)


        self.btn_creer_chambre = QPushButton("Créer une chambre", centralArea)
        self.btn_creer_chambre.setGeometry(10, 70, 270, 60)
        self.btn_creer_chambre.clicked.connect(self.ouvrir_creation_chambre)

        self.btn_voir_reservations = QPushButton("Voir les réservations", centralArea)
        self.btn_voir_reservations.setGeometry(290, 70, 270, 60)
        self.btn_voir_reservations.clicked.connect(self.ouvrir_liste_reservations)

        self.btn_prendre_res = QPushButton("Prendre une réservation", centralArea)
        self.btn_prendre_res.setGeometry(10, 140, 270, 60)
        self.btn_prendre_res.clicked.connect(self.ouvrir_prendre_reservation)

        self.btn_voir_chambres = QPushButton("Voir les chambres", centralArea)
        self.btn_voir_chambres.setGeometry(290, 140, 270, 60)
        self.btn_voir_chambres.clicked.connect(self.ouvrir_liste_chambres)

        self.fenetre_secondaire = None

  

    @Slot()
    def ouvrir_creation_chambre(self):
        self.fenetre_secondaire = VueCreerChambre()
        self.fenetre_secondaire.show()

    @Slot()
    def ouvrir_liste_reservations(self):
        self.fenetre_secondaire = VueReservationTotal()
        self.fenetre_secondaire.show()

    @Slot()
    def ouvrir_prendre_reservation(self):
        print("Bouton 'Prendre réservation' cliqué. (Classe vue à créer)")
       
    @Slot()
    def ouvrir_liste_chambres(self):
        self.fenetre_secondaire = VueChambreTot()
        self.fenetre_secondaire.show()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = VuePrincipale()
    main_win.show()
    sys.exit(app.exec())