from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QGridLayout
from PySide6.QtCore import Qt

class Services(QWidget):
    
    def label_creation(self, nom: str):
        label = QLabel(f"{nom}", self)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label.setFixedWidth(110) 
        return label

    def checkbox_creation(self):
        checkbox = QCheckBox("non", self)
        checkbox.setFixedWidth(60) 
        checkbox.setCursor(Qt.PointingHandCursor)
        checkbox.clicked.connect(lambda: self.changement_checkbox(checkbox))  
        return checkbox
        
    def __init__(self):
        super().__init__()

        label_spa = self.label_creation("Spa (8€/pers/jour)") 
        self.checkbox_spa = self.checkbox_creation()     
        label_petit_dej = self.label_creation("Petit Déjeuner (5€/pers/jour)") 
        self.checkBox_petit_dej = self.checkbox_creation()       
        label_wifi = self.label_creation("Wifi (3€/jour)") 
        self.checkBox_wifi = self.checkbox_creation()        
        label_parking = self.label_creation("Parking (10€/jour)") 
        self.checkBox_parking = self.checkbox_creation()
        label_fumeur = self.label_creation("Fumeur") 
        self.checkBox_fumeur = self.checkbox_creation()
        label_animaux = self.label_creation("Animaux") 
        self.checkBox_animaux = self.checkbox_creation()
        label_climatisation = self.label_creation("Climatisation") 
        self.checkBox_climatisation = self.checkbox_creation()
        
        layout_grille = QGridLayout()
        layout_grille.setSpacing(15) 

        layout_grille.addWidget(label_animaux, 0, 0)
        layout_grille.addWidget(self.checkBox_animaux, 0, 1)
        layout_grille.addWidget(label_fumeur, 0, 2)
        layout_grille.addWidget(self.checkBox_fumeur, 0, 3)
        layout_grille.addWidget(label_climatisation, 0, 4)
        layout_grille.addWidget(self.checkBox_climatisation, 0, 5)

        layout_grille.addWidget(label_petit_dej, 1, 0)
        layout_grille.addWidget(self.checkBox_petit_dej, 1, 1)
        layout_grille.addWidget(label_wifi, 1, 2)
        layout_grille.addWidget(self.checkBox_wifi, 1, 3)
        layout_grille.addWidget(label_spa, 1, 4)
        layout_grille.addWidget(self.checkbox_spa, 1, 5)
        layout_grille.addWidget(label_parking, 1, 6)
        layout_grille.addWidget(self.checkBox_parking, 1, 7)

        self.setLayout(layout_grille)

    def changement_checkbox(self, checkbox):
        if checkbox.isChecked():
            checkbox.setText("oui")
            checkbox.setStyleSheet("font-weight: bold; color: #4CAF50;")
        else:
            checkbox.setText("non")
            checkbox.setStyleSheet("font-weight: normal; color: black;")