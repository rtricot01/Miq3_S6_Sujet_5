import sys
from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, \
                             QPushButton, QCheckBox, QLineEdit, QVBoxLayout

from classe_objet import creer_chambre

class VueCreerChambre(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Création d'une Chambre")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(310, 300)

        centralArea = QWidget()
        self.setCentralWidget(centralArea)
        layout = QVBoxLayout(central_area)


        label = QLabel("Formulaire de création de chambre", centralArea)
        label.setGeometry(20, 10, 270, 20)

        layout.addWidget(QLabel("Capacité (nb personnes) :"))
        self.input_max_people = QLineEdit()
        self.input_max_people.setPlaceholderText("Ex : 3")
        layout.addWidget(self.input_max_people)

        layout.addWidget(QLabel("Prix de la nuit (€) :"))
        self.input_price = QLineEdit()
        self.input_price.setPlaceholderText("Ex : 85.50")
        layout.addWidget(self.input_price)

        layout.addWidget(QLabel("Superficie (m²) :"))
        self.input_size = QLineEdit()
        self.input_size.setPlaceholderText("Ex : 25")
        layout.addWidget(self.input_size)

        self.chk_fumeur = QCheckBox("Fumeur")
        self.chk_animaux = QCheckBox("Animaux acceptés")
        self.chk_clim = QCheckBox("Climatisation")
        layout.addWidget(self.chk_fumeur)
        layout.addWidget(self.chk_animaux)
        layout.addWidget(self.chk_clim)

        self.btn_valider = QPushButton("Enregistrer la chambre")
        self.btn_valider.clicked.connect(self.enregistrer_donnees)
        layout.addWidget(self.btn_valider)


       
    @Slot()
    def enregistrer_donnees(self):
        try:
            nb_pers = int(self.input_max_people.text())
            prix = float(self.input_price.text())
            taille = int(self.input_size.text())
            
            fumeur = self.chk_fumeur.isChecked()
            animaux = self.chk_animaux.isChecked()
            clim = self.chk_clim.isChecked()

            nouvelle_chambre = creer_chambre(nb_pers, prix, taille, fumeur, animaux, clim)

            print(f"Succées ! La Chambre a été créée avec l'ID : {nouvelle_chambre.room_id}")
            self.statusBar().showMessage(f"Chambre {nouvelle_chambre.room_id} enregistrée !", 5000)
            
            self.input_max_people.clear()
            self.input_price.clear()
            self.input_size.clear()

        except ValueError:
            print("Erreur : Veuillez entrer des données valides.")
            self.statusBar().showMessage("Erreur : Format incorrect.", 5000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ma_vue = VueCreerChambre()
    ma_vue.show()
    sys.exit(app.exec())