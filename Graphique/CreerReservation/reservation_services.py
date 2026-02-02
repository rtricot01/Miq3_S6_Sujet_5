from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout

class Services(QWidget):
    
    def label_creation(self, nom: str):
        label = QLabel(f"{nom}", self)
        label.setFixedWidth(100)
        return label

    def checkbox_creation(self):
        checkbox = QCheckBox("non", self)
        checkbox.setFixedWidth(50)
        checkbox.clicked.connect(lambda: self.changement_checkbox(checkbox))  
        return checkbox
        
    def __init__(self):
        super().__init__()

        label_piscine = self.label_creation("Piscine") 
        checkbox_piscine = self.checkbox_creation()     
        label_petit_dej = self.label_creation("Petit Déjeuner") 
        checkBox_petit_dej = self.checkbox_creation()       
        label_sauna = self.label_creation("Sauna") 
        checkBox_sauna = self.checkbox_creation()    
        label_hammam = self.label_creation("Hammam") 
        checkBox_hammam = self.checkbox_creation()    
        label_voiture = self.label_creation("Voiture") 
        checkBox_voiture = self.checkbox_creation()
        label_fumeur = self.label_creation("Fumeur") 
        checkBox_fumeur = self.checkbox_creation()
        label_animaux = self.label_creation("Animaux") 
        checkBox_animaux = self.checkbox_creation()
        label_climatisation = self.label_creation("Climatisation") 
        checkBox_climatisation = self.checkbox_creation()
        
        box_services1 = QHBoxLayout()
        box_services1.addWidget(label_animaux)
        box_services1.addWidget(checkBox_animaux)
        box_services1.addSpacing(30)
        box_services1.addWidget(label_fumeur)
        box_services1.addWidget(checkBox_fumeur)
        box_services1.addSpacing(30)
        box_services1.addWidget(label_climatisation)
        box_services1.addWidget(checkBox_climatisation)
        box_services1.addSpacing(30)
        box_services1.addWidget(label_voiture)
        box_services1.addWidget(checkBox_voiture)

        box_services2 = QHBoxLayout()
        box_services2.addWidget(label_petit_dej)
        box_services2.addWidget(checkBox_petit_dej)
        box_services2.addSpacing(30)
        box_services2.addWidget(label_piscine)
        box_services2.addWidget(checkbox_piscine)
        box_services2.addSpacing(30)
        box_services2.addWidget(label_sauna)
        box_services2.addWidget(checkBox_sauna)
        box_services2.addSpacing(30)
        box_services2.addWidget(label_hammam)
        box_services2.addWidget(checkBox_hammam)

        box_service = QVBoxLayout()
        box_service.addLayout(box_services1)
        box_service.setSpacing(20)
        box_service.addLayout(box_services2)

        self.setLayout(box_service)

    def changement_checkbox(self, checkbox):
        if checkbox.isChecked():
            checkbox.setText("oui")
        else:
            checkbox.setText("non")