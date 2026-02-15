from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QMessageBox, QHBoxLayout, QLineEdit, QComboBox)
from PySide6.QtCore import Signal, QDate, Qt
from PySide6.QtGui import QIcon
from src.hotel_manager.modele.exceptions import ReservationDateException, TooManyPeopleException
from src.hotel_manager.graphique.creer_reservation.reservation_calendrier import Calendrier
from src.hotel_manager.controleur.reservation_controller import suppression_reservation, modifier_reservation
from src.hotel_manager.modele.gestion_db import session_db, ChambreDB

class VueDetailReservation(QWidget):
    demande_rafraichissement = Signal()

    def __init__(self, reservation):
        super().__init__()
        self.res = reservation 
        self.setWindowTitle(f"Modification Réservation #{self.res.reservation_id}")
        self.setWindowIcon(QIcon("icone_chambre.png"))
        self.resize(500, 700)
        
        self.prix_nuit_chambre = 0.0
        with session_db() as session:
            chambre = session.query(ChambreDB).get(self.res.room_id)
            if chambre:
                self.prix_nuit_chambre = chambre.prize

        layout_principal = QVBoxLayout(self)

        layout_principal.addWidget(QLabel(f"<h2>Gestion de la Réservation N° {self.res.reservation_id}</h2>"))
        layout_principal.addWidget(QLabel(f"<b>Chambre :</b> {self.res.room_id} ({self.prix_nuit_chambre} €/nuit)"))
        layout_principal.addSpacing(10)

        layout_principal.addWidget(QLabel("<b>Dates de séjour :</b>"))
        self.comp_calendrier = Calendrier()
        self.comp_calendrier.calendrier_debut.setSelectedDate(
            QDate(self.res.start_date.year, self.res.start_date.month, self.res.start_date.day))
        self.comp_calendrier.calendrier_fin.setSelectedDate(
            QDate(self.res.end_date.year, self.res.end_date.month, self.res.end_date.day))
        
        self.comp_calendrier.calendrier_debut.selectionChanged.connect(self.calculer_prix)
        self.comp_calendrier.calendrier_fin.selectionChanged.connect(self.calculer_prix)
        layout_principal.addWidget(self.comp_calendrier)

        box_pers = QHBoxLayout()
        box_pers.addWidget(QLabel("Nombre de personnes :"))
        self.input_pers = QLineEdit(str(self.res.nombre_personnes))
        self.input_pers.textChanged.connect(self.calculer_prix)
        box_pers.addWidget(self.input_pers)
        layout_principal.addLayout(box_pers)

        layout_principal.addWidget(QLabel("<b>Services additionnels :</b>"))
        self.combos = {}
        services_config = [
            ("Spa (8€/pers/jour)", "spa"),
            ("Petit Déjeuner (5€/pers/jour)", "petit_dejeuner"),
            ("Parking (10€/jour)", "parking"),
            ("Wifi (3€/jour)", "wifi")
        ]

        for label_text, attr_name in services_config:
            box = QHBoxLayout()
            box.addWidget(QLabel(label_text))
            combo = QComboBox()
            combo.addItems(["Non", "Oui"])
            val = getattr(self.res, attr_name)
            combo.setCurrentIndex(1 if val else 0)
            combo.currentIndexChanged.connect(self.calculer_prix)
            self.combos[attr_name] = combo
            box.addWidget(combo)
            layout_principal.addLayout(box)

        self.label_prix_total = QLabel("Total : 0.00 €")
        self.label_prix_total.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin: 15px;")
        self.label_prix_total.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.label_prix_total)

        box_btn = QHBoxLayout()
        btn_modif = QPushButton("Enregistrer")
        btn_modif.clicked.connect(self.modifier_action)
        btn_modif.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        
        btn_suppr = QPushButton("Supprimer")
        btn_suppr.clicked.connect(self.confirmer_suppression)
        btn_suppr.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        
        box_btn.addWidget(btn_modif)
        box_btn.addWidget(btn_suppr)
        layout_principal.addLayout(box_btn)

        self.calculer_prix()

    def calculer_prix(self):
        """Même formule que dans vue_reservation.py"""
        try:
            d_debut = self.comp_calendrier.calendrier_debut.selectedDate().toPython()
            d_fin = self.comp_calendrier.calendrier_fin.selectedDate().toPython()
            
            if d_fin <= d_debut:
                self.label_prix_total.setText("Dates invalides")
                return

            nb_nuits = (d_fin - d_debut).days
            try:
                nb_pers = int(self.input_pers.text())
            except:
                nb_pers = 0

            total = self.prix_nuit_chambre * nb_nuits
            
            if self.combos["spa"].currentIndex() == 1:
                total += (8 * nb_pers * nb_nuits)
            if self.combos["petit_dejeuner"].currentIndex() == 1:
                total += (5 * nb_pers * nb_nuits)
            if self.combos["wifi"].currentIndex() == 1:
                total += (3 * nb_nuits)
            if self.combos["parking"].currentIndex() == 1:
                total += (10 * nb_nuits)

            self.label_prix_total.setText(f"Total estimé : {round(total, 2)} €")
        except Exception as e:
            print(f"Erreur calcul : {e}")

    def modifier_action(self):
        try:
            d_debut = self.comp_calendrier.calendrier_debut.selectedDate().toPython()
            d_fin = self.comp_calendrier.calendrier_fin.selectedDate().toPython()
            
            modifier_reservation(
                id_res=self.res.reservation_id,
                id_room=self.res.room_id,
                nombre_pers=int(self.input_pers.text()),
                date_debut=d_debut,
                date_fin=d_fin,
                spa=self.combos["spa"].currentIndex() == 1,
                petit_dej=self.combos["petit_dejeuner"].currentIndex() == 1,
                parking=self.combos["parking"].currentIndex() == 1,
                wifi=self.combos["wifi"].currentIndex() == 1
            )
            QMessageBox.information(self, "Succès", "Réservation modifiée !")
            self.demande_rafraichissement.emit()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Modification impossible : {e}")

    def confirmer_suppression(self):
        if QMessageBox.question(self, "Attention", "Annuler cette réservation ?", 
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            suppression_reservation(self.res.reservation_id)
            self.demande_rafraichissement.emit()
            self.close()