from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                               QMessageBox, QHBoxLayout, QLineEdit, QComboBox)
from PySide6.QtCore import Signal, QDate
from hotel_manager.modele.exceptions import ReservationDateException, TooManyPeopleException
from hotel_manager.graphique.creer_reservation.reservation_calendrier import Calendrier
from hotel_manager.controleur.reservation_controller import suppression_reservation, modifier_reservation

class VueDetailReservation(QWidget):
    demande_rafraichissement = Signal()

    def __init__(self, reservation):
        super().__init__()
        self.res = reservation 
        self.setWindowTitle(f"Modification Réservation #{self.res.reservation_id}")
        self.resize(500, 600)
        
        layout_principal = QVBoxLayout(self)

        layout_principal.addWidget(QLabel(f"<h2>Gestion de la Réservation N° {self.res.reservation_id}</h2>"))
        layout_principal.addWidget(QLabel(f"<b>Chambre :</b> {self.res.room_id}"))
        layout_principal.addSpacing(10)

        layout_principal.addWidget(QLabel("<b>Dates de séjour :</b>"))
        self.comp_calendrier = Calendrier()
        self.comp_calendrier.calendrier_debut.setSelectedDate(
            QDate(self.res.start_date.year, self.res.start_date.month, self.res.start_date.day))
        self.comp_calendrier.calendrier_fin.setSelectedDate(
            QDate(self.res.end_date.year, self.res.end_date.month, self.res.end_date.day))
        layout_principal.addWidget(self.comp_calendrier)

        row_pers = QHBoxLayout()
        row_pers.addWidget(QLabel("<b>Nombre de personnes :</b>"))
        self.input_pers = QLineEdit(str(self.res.nombre_personnes))
        self.input_pers.setFixedWidth(60)
        row_pers.addWidget(self.input_pers)
        row_pers.addStretch()
        layout_principal.addLayout(row_pers)

        layout_principal.addSpacing(15)
        layout_principal.addWidget(QLabel("<h3>Options de services </h3>"))

        """Je mets que les options modifiables, pas liée à la chambre"""

        self.combos = {}
        options_client = [
            ("Petit Déjeuner", "petit_dejeuner"),
            ("Accès Spa", "spa"),
            ("Place de Parking", "parking"),
            ("Accès WiFi", "wifi")
        ]

        for label_text, attr in options_client:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            
            combo = QComboBox()
            combo.addItems(["Non", "Oui"])
            
            valeur_actuelle = getattr(self.res, attr, False)
            combo.setCurrentIndex(1 if valeur_actuelle else 0)
            
            self.combos[attr] = combo
            row.addWidget(combo)
            layout_principal.addLayout(row)

        layout_principal.addStretch()

        btn_layout = QHBoxLayout()
        
        btn_save = QPushButton("Enregistrer les modifications")
        btn_save.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-weight: bold;")
        btn_save.clicked.connect(self.sauvegarder)

        btn_del = QPushButton("Annuler la réservation")
        btn_del.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        btn_del.clicked.connect(self.confirmer_suppression)

        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_del)
        layout_principal.addLayout(btn_layout)
        self.comp_calendrier.date_debut.setText(self.res.start_date.strftime("%d/%m/%Y"))
        self.comp_calendrier.date_fin.setText(self.res.end_date.strftime("%d/%m/%Y"))
        self.comp_calendrier.calendrier_debut.showSelectedDate()
        self.comp_calendrier.calendrier_fin.showSelectedDate()

    def sauvegarder(self):
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
            
            QMessageBox.information(self, "OK", "Réservation mise à jour.")
            self.demande_rafraichissement.emit()
            self.close()
            
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Vérifiez le nombre de personnes.")
        except TooManyPeopleException:
            QMessageBox.warning(self, "Capacité", "Trop de personnes pour cette chambre !")
        except ReservationDateException as e:
            QMessageBox.warning(self, "Dates", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def confirmer_suppression(self):
        if QMessageBox.question(self, "Confirmation", "Annuler définitivement ?", 
                                 QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            suppression_reservation(self.res.reservation_id)
            self.demande_rafraichissement.emit()
            self.close()