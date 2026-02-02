from PySide6.QtWidgets import  QWidget, QLabel, QSlider, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import  Qt


class Prix (QWidget):

    def __init__(self, prix_journee_maximal:float):
        super().__init__()

        self.label_prix_maximal = QLabel(f"Prix maximal :  {prix_journee_maximal}", self)
        self.label_prix_maximal.resize(270, 30)
        self.slider_prix_maximal = QSlider(Qt.Horizontal, self)
        self.slider_prix_maximal.setRange(0,prix_journee_maximal)
        self.slider_prix_maximal.setValue(0.8 * prix_journee_maximal)
        self.slider_prix_maximal.resize(400, 50)
        

        self.label_prix_minimal = QLabel(f"Prix minimal :  {0}", self)
        self.label_prix_minimal.resize(270, 30)
        self.slider_prix_minimal = QSlider(Qt.Horizontal, self)
        self.slider_prix_minimal.setRange(0,prix_journee_maximal)
        self.slider_prix_minimal.setValue(0)
        self.slider_prix_minimal.resize(400, 50)

        box_prix_minimal = QHBoxLayout()
        box_prix_minimal.addWidget(self.label_prix_minimal)
        box_prix_minimal.setSpacing(10)
        box_prix_minimal.addWidget(self.slider_prix_minimal)

        box_prix_maximal = QHBoxLayout()
        box_prix_maximal.addWidget(self.label_prix_maximal)
        box_prix_maximal.setSpacing(10)
        box_prix_maximal.addWidget(self.slider_prix_maximal)

        box_prix = QVBoxLayout()
        box_prix.addLayout(box_prix_maximal)
        box_prix.setSpacing(20)
        box_prix.addLayout(box_prix_minimal)

        self.setLayout(box_prix)

        self.slider_prix_maximal.valueChanged.connect(self.changement_valeur)
        self.slider_prix_minimal.valueChanged.connect(self.changement_valeur)

    def changement_valeur(self):
        valeur_min = self.slider_prix_minimal.value()
        valeur_max = self.slider_prix_maximal.value()

        if valeur_min > valeur_max:
            if self.sender() == self.slider_prix_minimal:
                self.slider_prix_maximal.setValue(valeur_min)
            else:
                self.slider_prix_minimal.setValue(valeur_max)

        self.label_prix_maximal.setText(f"Prix maximale : {self.slider_prix_maximal.value()}")
        self.label_prix_minimal.setText(f"Prix minimale : {self.slider_prix_minimal.value()}")














        
