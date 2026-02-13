from PySide6.QtWidgets import  QWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout


class NombrePersonne (QWidget):

    def __init__(self):
        super().__init__()

        label_enfant = QLabel("Nombre d'enfant : ", self)
        label_enfant.resize(270, 30)
        self.textBox_nbr_enfant = QLineEdit("0", self)
        self.textBox_nbr_enfant.resize(270, 30)

        label_adulte = QLabel("Nombre d'adulte : ", self)
        label_adulte.resize(270, 30)
        self.textBox_nbr_adulte = QLineEdit("0", self)
        self.textBox_nbr_adulte.resize(270, 30)

        box_enfant = QHBoxLayout()
        box_enfant.addWidget(label_enfant)
        box_enfant.setSpacing(10)
        box_enfant.addWidget(self.textBox_nbr_enfant)

        box_adulte = QHBoxLayout()
        box_adulte.addWidget(label_adulte)
        box_adulte.setSpacing(20)
        box_adulte.addWidget(self.textBox_nbr_adulte)

        box_personne = QVBoxLayout()
        box_personne.addLayout(box_adulte)
        box_personne.setSpacing(10)
        box_personne.addLayout(box_enfant)

        self.setLayout(box_personne)

