import sys
from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QTableWidget, 
                             QTableWidgetItem, QApplication, QMainWindow, QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from Gestion_db import Session, ChambreDB, OptionChambreDB, OptionsChambrePossibles

class VueChambreTot(QMainWindow):

    def __init__(self, parent=None):
        super(VueChambreTot, self).__init__(parent)
        self.setWindowTitle("Gestion des Chambres - Hôtel")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(800, 450)

        central_area = QWidget()
        self.setCentralWidget(central_area)
        main_layout = QVBoxLayout(central_area)

        self.label = QLabel("Liste des Chambres")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        main_layout.addWidget(self.label)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Capacité", "Prix (€)", "Superficie (m²)", 
            "Clim", "Fumeur", "Animaux"
        ])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.charger_donnees()
        

   def charger_donnees(self):
        with Session() as session:
            chambres = session.query(ChambreDB).all()
            self.table.setRowCount(len(chambres))

            for row, chambre in enumerate(chambres):
                options_db = session.query(OptionChambreDB).filter_by(room_id=chambre.room_id).all()
                ids_actifs = [opt.option_chambre_id for opt in options_db]

                self.table.setItem(row, 0, QTableWidgetItem(str(chambre.room_id)))
                self.table.setItem(row, 1, QTableWidgetItem(str(chambre.max_people)))
                self.table.setItem(row, 2, QTableWidgetItem(str(chambre.prize)))
                self.table.setItem(row, 3, QTableWidgetItem(str(chambre.room_size)))

                clim = "Oui" if OptionsChambrePossibles.CLIMATISATION in ids_actifs else "Non"
                fumeur = "Oui" if OptionsChambrePossibles.FUMEUR in ids_actifs else "Non"
                animaux = "Oui" if OptionsChambrePossibles.ANIMAUX_TOLERES in ids_actifs else "Non"

                self.table.setItem(row, 4, QTableWidgetItem(clim))
                self.table.setItem(row, 5, QTableWidgetItem(fumeur))
                self.table.setItem(row, 6, QTableWidgetItem(animaux))

                for col in range(7):
                    item = self.table.item(row, col)
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(Qt.ItemIsEnabled)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VueChambreTot()
    window.show()
    sys.exit(app.exec())