from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QScrollArea, QLabel, QLineEdit, QMessageBox

from datetime import datetime

from hotel_manager.controleur.reservation_controller import creer_reservation
from hotel_manager.graphique.creer_reservation.chambre_select import ChambreSelect
from hotel_manager.modele import classe_objet

from .reservation_calendrier import Calendrier
from .reservation_prix import Prix
from .reservation_personne import NombrePersonne
from .reservation_services import Services

from hotel_manager.controleur.client_controller import afficher_tous_les_clients, creer_client
from hotel_manager.modele.gestion_db import session_db, ChambreDB 

class FenetreReservation (QMainWindow):

    def __init__(self,parent=None):
        self.PRIX_MAX_HOTEL = float(self.get_max_price_from_db())

        super(FenetreReservation, self).__init__(parent)

        self.setWindowTitle("Réservation d'une Chambre")
        self.setWindowIcon(QIcon("icone_chambre.png"))
        self.showMaximized()
        fenetre_principale = QWidget()
        fenetre_principale.setStyleSheet("background: #C6B7D1")
        self.setCentralWidget(fenetre_principale)

        self.layout_global = QVBoxLayout (fenetre_principale)
        layout_top = QHBoxLayout()

        bouton_valider = QPushButton("Valider")
        bouton_valider.clicked.connect(self.action_bouton)

        self.calendrier = Calendrier()
        self.prix = Prix(self.PRIX_MAX_HOTEL)
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

        if self.chambre_selectionnee:
            self.chambre_selectionnee.set_normal_style()
        
        self.chambre_selectionnee = widget
        self.chambre_selectionnee.set_selected_style()
        
        if not self.bouton_reserver:
            self.bouton_reserver = QPushButton("Confirmer la Réservation")
            self.bouton_reserver.setStyleSheet("background-color: #4CAF50; color: white; height: 50px; font-weight: bold;")
            self.bouton_reserver.clicked.connect(self.finaliser_reservation)
            self.layout_global.addWidget(self.bouton_reserver)

    def action_bouton(self):
        try:
            texte_debut = self.calendrier.date_debut.text()
            texte_fin = self.calendrier.date_fin.text()
            
            self.date_debut_obj = datetime.strptime(texte_debut, "%d/%m/%Y").date()
            self.date_fin_obj = datetime.strptime(texte_fin, "%d/%m/%Y").date()

            nb_a = int(self.personne.textBox_nbr_adulte.text() or 0)
            nb_e = int(self.personne.textBox_nbr_enfant.text() or 0)
            self.min_people_total = nb_a + nb_e

            fumeur = self.services.checkBox_fumeur.isChecked()
            animaux = self.services.checkBox_animaux.isChecked()
            clim = self.services.checkBox_climatisation.isChecked()
            p_min = self.prix.slider_prix_minimal.value()
            p_max = self.prix.slider_prix_maximal.value()

            chambres_disponibles = classe_objet.recuperer_chambre_libre_db(
                self.date_debut_obj, self.date_fin_obj, self.min_people_total, 
                fumeur, animaux, clim, p_min, p_max
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

            form_client = QHBoxLayout()
            self.input_nom = QLineEdit(); self.input_nom.setPlaceholderText("Nom")
            self.input_prenom = QLineEdit(); self.input_prenom.setPlaceholderText("Prénom")
            self.input_tel = QLineEdit(); self.input_tel.setPlaceholderText("Téléphone")
            self.input_mail = QLineEdit(); self.input_mail.setPlaceholderText("Email")
            
            for w in [self.input_nom, self.input_prenom, self.input_tel, self.input_mail]:
                w.setStyleSheet("padding: 8px; background: white; border-radius: 5px; color: black;")
                form_client.addWidget(w)
            
            self.layout_global.addLayout(form_client)

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

        except ValueError as e:
            QMessageBox.warning(self, "Erreur de saisie", "Vérifiez le format des dates (JJ/MM/AAAA) ou des nombres.")
        except Exception as e:
            print(f"Erreur : {e}")

    

    def finaliser_reservation(self):
        if not self.chambre_selectionnee:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une chambre.")
            return

        # 1. Récupération des saisies
        nom = self.input_nom.text().strip().upper() # On normalise en majuscules pour la comparaison
        prenom = self.input_prenom.text().strip()
        tel = self.input_tel.text().strip()
        mail = self.input_mail.text().strip()

        if not all([nom, prenom, tel, mail]):
            QMessageBox.warning(self, "Erreur", "Veuillez remplir toutes les informations client (Nom, Prénom, Tel, Mail).")
            return

        try:
            id_client_final = None
            clients_existants = afficher_tous_les_clients()
        
            for c in clients_existants:
                if (c.client_lastname.upper() == nom and 
                    c.client_firstname == prenom and 
                    c.client_tel == tel and 
                    c.client_mail == mail):
                    id_client_final = c.client_id
                    break
        
            if id_client_final is None:
                nouveau_client = creer_client(prenom, nom, tel, mail)
                id_client_final = nouveau_client.client_id

            creer_reservation(
                id_room=self.chambre_selectionnee.data.room_id,
                id_client=id_client_final,
                nombre_personnes=self.min_people_total, 
                date_start=self.date_debut_obj,
                date_end=self.date_fin_obj,
                spa=self.etat_spa, 
                petit_dejeuner=self.etat_petit_dej,
                parking=self.etat_parking,
                wifi=self.etat_wifi
            )

            QMessageBox.information(self, "Succès", f"Réservation confirmée pour M./Mme {nom} !")
            self.close() 

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la réservation : {e}")