from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class ChambreSelect(QFrame):
    def __init__(self, data, parent_window, parent=None):
        super().__init__(parent)
        self.data = data
        self.parent_window = parent_window
        self.selected = False
        self.setFixedSize(300, 450)
        self.set_normal_style()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel(f"<b>Chambre n°{self.data.room_id}</b>")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px;")
        
        fumeur_txt = "Oui" if self.data.fumeur else "Non"
        clim_txt = "Oui" if self.data.climatisation else "Non"
        animaux_txt = "Acceptés" if self.data.animaux_toleres else "Refusés"

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(QLabel(f"<b>Prix :</b> {self.data.price} € / nuit"))
        layout.addWidget(QLabel(f"<b>Capacité :</b> {self.data.max_people} pers."))
        layout.addWidget(QLabel(f"<b>Surface :</b> {self.data.room_size} m²"))
        layout.addSpacing(10)
        layout.addWidget(QLabel(f"Fumeur : {fumeur_txt}"))
        layout.addWidget(QLabel(f"Climatisation : {clim_txt}"))
        layout.addWidget(QLabel(f"Animaux : {animaux_txt}"))
        
        layout.addStretch()
    
    def set_normal_style(self):
        self.selected = False
        self.setStyleSheet("QFrame { background-color: #E6E0ED; border-radius: 15px; border: 2px solid #A084B7; }")

    def set_selected_style(self):
        self.selected = True
        self.setStyleSheet("QFrame { background-color: #E6E0ED; border-radius: 15px; border: 4px solid #4CAF50; }") # Bordure verte épaisse

    def mousePressEvent(self, event):
        self.parent_window.selectionner_chambre(self)