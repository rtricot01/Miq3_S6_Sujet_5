from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QLineEdit, QMessageBox

from datetime import datetime

from src.hotel_manager.controleur.reservation_controller import creer_reservation
from src.hotel_manager.graphique.creer_reservation.chambre_select import ChambreSelect
from src.hotel_manager.modele import classe_objet
from src.hotel_manager.modele.exceptions import ClientMissingDataException, RoomNotSelectedException

from .reservation_calendrier import Calendrier
from .reservation_prix import Prix
from .reservation_personne import NombrePersonne
from .reservation_services import Services

import logging

from src.hotel_manager.controleur.client_controller import afficher_tous_les_clients, creer_client
from src.hotel_manager.modele.gestion_db import session_db, ChambreDB 
from src.hotel_manager.controleur.controle_saisie import controler_nombre_personnes, controler_nombre_adultes

class FenetreReservation (QMainWindow):

    def __init__(self,parent=None):
        self.prix_chambre_max = float(self.get_max_price_from_db())

        super(FenetreReservation, self).__init__(parent)

        self.setWindowTitle("Réservation d'une Chambre")
        self.setWindowIcon(QIcon("icone_chambre.png"))
        # self.showMaximized()

        fenetre_principale = QWidget()
        fenetre_principale.setStyleSheet("background: #C6B7D1")
        self.setCentralWidget(fenetre_principale)

        self.layout_global = QVBoxLayout (fenetre_principale)
        layout_top = QHBoxLayout()

        bouton_valider = QPushButton("Valider")
        bouton_valider.clicked.connect(self.action_bouton)

        self.calendrier = Calendrier()
        self.prix = Prix(self.prix_chambre_max)
        self.personne = NombrePersonne()
        self.services = Services()

        self.layout_global.addWidget(self.services)
        
        layout_top.setSpacing(40)
        layout_top.addWidget(self.calendrier)
        layout_top.addWidget(self.prix)
        layout_top.addWidget(self.personne)

        self.layout_global.addLayout(layout_top)
        self.layout_global.setSpacing(20)
        self.layout_global.addWidget(self.services)
        self.layout_global.addWidget(bouton_valider)

        self.scroll_resultats = None
        self.chambre_selectionnee = None
        self.bouton_reserver = None
    
    def get_max_price_from_db(self):
        try:
            with session_db() as session:
                from sqlalchemy import func
                max_p = session.query(func.max(ChambreDB.prize)).scalar()
                return float(max_p) if max_p is not None else 500.0
        except Exception as e:
            print(f"Erreur recup prix max : {e}")
            return 500.0 

    def nettoyer_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self.nettoyer_layout(item.layout())
    
    def selectionner_chambre(self, widget):
        try:
            if self.chambre_selectionnee:
                self.chambre_selectionnee.set_normal_style()
        
            self.chambre_selectionnee = widget
            self.chambre_selectionnee.set_selected_style()
        
            if not self.bouton_reserver:
                self.bouton_reserver = QPushButton("Confirmer la Réservation")
                self.bouton_reserver.setStyleSheet("background-color: #4CAF50; color: white; height: 50px; font-weight: bold;")
                self.bouton_reserver.clicked.connect(self.finaliser_reservation)
                self.layout_global.addWidget(self.bouton_reserver)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Reservation impossible : {e}")

    def action_bouton(self):

        try:
            texte_debut = self.calendrier.date_debut.text()
            texte_fin = self.calendrier.date_fin.text()
            
            self.date_debut_obj = datetime.strptime(texte_debut, "%d/%m/%Y").date()
            self.date_fin_obj = datetime.strptime(texte_fin, "%d/%m/%Y").date()

            nombre_adulte = int(self.personne.textBox_nbr_adulte.text() or 0)

            controler_nombre_adultes(nombre_adulte)
            nombre_enfant = int(self.personne.textBox_nbr_enfant.text() or 0)
            self.min_personne_total = nombre_adulte + nombre_enfant
            controler_nombre_personnes(self.min_personne_total)


            fumeur = self.services.checkBox_fumeur.isChecked()
            animaux = self.services.checkBox_animaux.isChecked()
            clim = self.services.checkBox_climatisation.isChecked()
            prix_min = self.prix.slider_prix_minimal.value()
            prix_max = self.prix.slider_prix_maximal.value()

            chambres_disponibles = classe_objet.recuperer_chambre_libre_db(
                self.date_debut_obj, self.date_fin_obj, self.min_personne_total, 
                fumeur, animaux, clim, prix_min, prix_max
            )

            self.etat_wifi = self.services.checkBox_wifi.isChecked()
            self.etat_spa = self.services.checkbox_spa.isChecked()
            self.etat_parking = self.services.checkBox_parking.isChecked()
            self.etat_petit_dej = self.services.checkBox_petit_dej.isChecked()
            self.etat_fumeur = self.services.checkBox_fumeur.isChecked()
            self.etat_animaux = self.services.checkBox_animaux.isChecked()
            self.etat_climatisation = self.services.checkBox_climatisation.isChecked()

            self.nettoyer_layout(self.layout_global)
            self.bouton_reserver = None 
            self.chambre_selectionnee = None

            informations_client = QHBoxLayout()
            self.nom = QLineEdit()
            self.nom.setPlaceholderText("Nom")
            self.prenom = QLineEdit()
            self.prenom.setPlaceholderText("Prénom")
            self.telephone = QLineEdit()
            self.telephone.setPlaceholderText("Téléphone")
            self.mail = QLineEdit()
            self.mail.setPlaceholderText("Email")
            
            for i in [self.nom, self.prenom, self.telephone, self.mail]:
                i.setStyleSheet("padding: 8px; background: white; border-radius: 5px; color: black;")
                informations_client.addWidget(i)
            
            self.layout_global.addLayout(informations_client)

            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setStyleSheet("border: none; background: transparent;")
            
            conteneur = QWidget()
            layout_h = QHBoxLayout(conteneur)

            if not chambres_disponibles:
                layout_h.addWidget(QLabel("Aucune chambre disponible pour ces critères."))
            else:
                for data in chambres_disponibles:
                    card = ChambreSelect(data, self) 
                    layout_h.addWidget(card)
            
            layout_h.addStretch()
            scroll.setWidget(conteneur)
            self.layout_global.addWidget(scroll)

        except ValueError:
            QMessageBox.warning(self, "Erreur de saisie", "Vérifiez le format des dates (JJ/MM/AAAA) ou des nombres.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Reservation impossible : {e}")

    

    def finaliser_reservation(self):
        try:
            if not self.chambre_selectionnee:
                raise RoomNotSelectedException

            nom = self.nom.text().strip().upper() 
            prenom = self.prenom.text().strip()
            telephone = self.telephone.text().strip()
            mail = self.mail.text().strip()

            if not all([nom, prenom, telephone, mail]):
                raise ClientMissingDataException
        
            id_client_final = None
            clients_existants = afficher_tous_les_clients()
        
            for i in clients_existants:
                if (i.client_lastname.upper() == nom and 
                    i.client_firstname == prenom and 
                    i.client_tel == telephone and 
                    i.client_mail == mail):
                    id_client_final = i.client_id
                    break
        
            if id_client_final is None:
                nouveau_client = creer_client(prenom, nom, telephone, mail)
                id_client_final = nouveau_client.client_id

            creer_reservation(
                id_room=self.chambre_selectionnee.data.room_id,
                id_client=id_client_final,
                nombres_personnes=self.min_personne_total, 
                date_start=self.date_debut_obj,
                date_end=self.date_fin_obj,
                spa=self.etat_spa, 
                petit_dejeuner=self.etat_petit_dej,
                parking=self.etat_parking,
                wifi=self.etat_wifi
            )

            prix_total = self.chambre_selectionnee.data.price * (self.date_fin_obj - self.date_debut_obj).days + (8*self.min_personne_total if self.etat_spa else 0).days + (5*self.min_personne_total if self.etat_petit_dej else 0).days + (3 if self.etat_wifi else 0).days + (10 if self.etat_parking else 0).days
            prix_total = round(prix_total, 2)
            QMessageBox.information(self, "Succès", f"Réservation confirmée pour M./Mme {nom} !\nPrix total : {prix_total} €")
            logging.info("Succès", f"Réservation confirmée pour M./Mme {nom} !\nPrix total : {prix_total} €")
            self.close() 

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la réservation : {e}")