from PySide6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
                               QScrollArea, QMainWindow)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from hotel_manager.modele.gestion_db import session_db, ReservationDB, ClientDB
from hotel_manager.graphique.vue_detail_reservation import VueDetailReservation

class VueReservationTotal(QMainWindow):
    changeItem = Signal(list)

    def __init__(self, items=None, parent=None):
        super(VueReservationTotal, self).__init__(parent)
        self.setWindowTitle("Gestion des Réservations - Hôtel")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(500, 400)

        central_area = QWidget()
        self.setCentralWidget(central_area)
        self.main_layout = QVBoxLayout(central_area)

        self.label = QLabel("Liste des Réservations")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        self.main_layout.addWidget(self.label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll_layout = QVBoxLayout(self.container)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.container)

        self.listItem = items if items is not None else self.recuperer_reservations_db()
        self.initUI()

    def recuperer_reservations_db(self):
        with session_db() as session:
            resultats = session.query(ReservationDB, ClientDB).join(
                ClientDB, ReservationDB.client_id == ClientDB.client_id
            ).all()
            return resultats
        
    def initUI(self):
        for i in reversed(range(self.scroll_layout.count())): 
            widget = self.scroll_layout.itemAt(i).widget()
            if widget: 
                widget.setParent(None)

        for res, client in self.listItem:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            
            infos = f"<b>#{res.reservation_id}</b> | {client.client_firstname} {client.client_lastname} (Chambre {res.room_id})"
            row_layout.addWidget(QLabel(infos))
            
            btn_detail = QPushButton("Détails")
            btn_detail.clicked.connect(lambda checked=False, r=res: self.ouvrir_detail(r))
            
            row_layout.addWidget(btn_detail)
            self.scroll_layout.addWidget(row_widget)

    def ouvrir_detail(self, reservation_obj):
        self.fenetre_detail = VueDetailReservation(reservation_obj)
        self.fenetre_detail.demande_rafraichissement.connect(self.rafraichir_liste)
        self.fenetre_detail.show()

    def rafraichir_liste(self):
        self.listItem = self.recuperer_reservations_db()
        self.initUI()
