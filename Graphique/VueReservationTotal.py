from PySide6.QtWidgets import (QWidget, QLabel, QCheckBox, QVBoxLayout, 
                             QScrollArea, QApplication, QMainWindow)
from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QIcon
import sys

from Gestion_db import Session, ReservationDB, ClientDB

class VueReservationTotal(QMainWindow):
    changeItem = Signal(list)

    def __init__(self, items=None, parent=None):
        super(VueReservationTotal, self).__init__(parent)
        self.setWindowTitle("Gestion des Réservations - Hôtel")
        self.setWindowIcon(QIcon("hotel.jpg"))
        self.resize(500, 400)

        central_area = QWidget()
        self.setCentralWidget(central_area)
        main_layout = QVBoxLayout(central_area)

        self.label = QLabel("Liste des Réservations")
        self.label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px;")
        main_layout.addWidget(self.label)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        main_layout.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll_layout = QVBoxLayout(self.container)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.container)

        self.listItem = items if items is not None else self.recuperer_reservations_db()
        self.listState = [False] * len(self.listItem)
        self.itemChk = []

        self.initUI()

    def recuperer_reservations_db(self):
        with Session() as session:
            resultats = session.query(ReservationDB, ClientDB).join(
                ClientDB, ReservationDB.client_id == ClientDB.client_id
            ).all()
            return resultats
        
    def initUI(self): 

        for i in reversed(range(self.scroll_layout.count())): 
            self.scroll_layout.itemAt(i).widget().setParent(None)

        if not self.listItem:
            self.scroll_layout.addWidget(QLabel("Aucune réservation trouvée."))
            return

        for i, (res, client) in enumerate(self.listItem):
            texte = (f"Réf: {res.reservation_id} | {client.client_firstname} {client.client_lastname} "
                     f"| Du {res.start_date} au {res.end_date}")
            
            chk = QCheckBox(texte)
            chk.stateChanged.connect(self.changeChk)
            
            chk.setProperty("index", i)
            
            self.itemChk.append(chk)
            self.scroll_layout.addWidget(chk)
        
    
    def changeChk(self, state):
        sender = self.sender()
        index = sender.property("index")
        is_checked = state > 0
        
        if index is not None:
            self.listState[index] = is_checked
            print(f"Réservation {index} cochée : {is_checked}")
        
        self.changeItem.emit(self.listState)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VueReservationTotal()
    window.show()
    sys.exit(app.exec())
