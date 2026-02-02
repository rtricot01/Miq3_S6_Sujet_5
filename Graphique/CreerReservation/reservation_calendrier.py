from PySide6.QtWidgets import QWidget, QCalendarWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QTextCharFormat, QFont, QColor
from PySide6.QtCore import Qt

class Calendrier(QWidget):
    
    def __init__(self, parent=None): 
        super().__init__(parent)

        self.ancienne_date_debut = None
        self.ancienne_date_fin = None

        self.calendrier_debut = QCalendarWidget(self)
        self.calendrier_fin = QCalendarWidget(self)

        box_date_debut = QHBoxLayout()
        self.label_date_debut = QLabel("Date de début:", self)
        self.date_debut = QLineEdit(self)

        box_date_fin = QHBoxLayout()
        self.label_date_fin = QLabel("Date de fin:", self)
        self.date_fin = QLineEdit(self)

        box_date_debut.addWidget(self.label_date_debut)
        box_date_debut.addWidget(self.date_debut)
        box_date_fin.addWidget(self.label_date_fin)
        box_date_fin.addWidget(self.date_fin)

        box_horizontal_dates = QHBoxLayout()
        box_horizontal_dates.addLayout(box_date_debut)
        box_horizontal_dates.addSpacing(20)
        box_horizontal_dates.addLayout(box_date_fin)

        box_calendrier = QHBoxLayout()
        box_calendrier.addWidget(self.calendrier_debut)
        box_calendrier.addWidget(self.calendrier_fin)

        layout_principal = QVBoxLayout()
        layout_principal.addLayout(box_calendrier)
        layout_principal.addSpacing(10)
        layout_principal.addLayout(box_horizontal_dates)

        self.setLayout(layout_principal)

        self.calendrier_debut.selectionChanged.connect(self.actionneur_date)
        self.calendrier_fin.selectionChanged.connect(self.actionneur_date)
    
    def typo_case(self, couleur: str):
        format_case = QTextCharFormat()
        format_case.setFontWeight(QFont.Weight.Bold)
        format_case.setBackground(QColor(couleur))
        format_case.setForeground(QColor("white")) 
        return format_case 

    def actionneur_date(self):
        envoyeur = self.sender()
        
        if envoyeur == self.calendrier_debut:
            widget_texte = self.date_debut
            ancienne_date = self.ancienne_date_debut
        else:
            widget_texte = self.date_fin
            ancienne_date = self.ancienne_date_fin

        date_selectionnee = envoyeur.selectedDate()
        string_date = date_selectionnee.toString("dd/MM/yyyy")
        couleur = "#86459C"

        if ancienne_date:
            envoyeur.setDateTextFormat(ancienne_date, QTextCharFormat())

        envoyeur.setDateTextFormat(date_selectionnee, self.typo_case(couleur))
        widget_texte.setText(string_date)

        if envoyeur == self.calendrier_debut:
            self.ancienne_date_debut = date_selectionnee
        else:
            self.ancienne_date_fin = date_selectionnee