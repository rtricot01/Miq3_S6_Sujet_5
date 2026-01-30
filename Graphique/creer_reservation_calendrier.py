from PySide6.QtWidgets import QWidget, QCalendarWidget, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QTextCharFormat, QFont, QColor

class Calendrier (QWidget):

    def __init__(self, parent=None): 
        super().__init__(parent)

        self.calendrier_debut = QCalendarWidget(self)
        self.calendrier_debut.resize(300, 200)
        self.calendrier_fin = QCalendarWidget(self)
        self.calendrier_fin.resize(300, 200)

        box_date_debut = QHBoxLayout()
        self.label_date_debut = QLabel("Date de début:", self)
        self.label_date_debut.resize(270, 30)
        self.date_debut = QLineEdit(None, self)
        self.date_debut.resize(300, 50)

        box_date_fin = QHBoxLayout()
        self.label_date_fin = QLabel("Date de fin:", self)
        self.label_date_fin.resize(270, 30)
        self.date_fin = QLineEdit(None, self)
        self.date_fin.resize(300, 50)

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

        box_vertical_calendrier_dates = QVBoxLayout()
        box_vertical_calendrier_dates.addLayout(box_calendrier)
        box_vertical_calendrier_dates.addSpacing(10)
        box_vertical_calendrier_dates.addLayout(box_horizontal_dates)

        self.setLayout(box_vertical_calendrier_dates)

        self.calendrier_debut.selectionChanged.connect(self.actionneur_date_debut)
        self.calendrier_fin.selectionChanged.connect(self.actionneur_date_fin)

    def actionneur_date_debut (self) : 
        date_de_debut = self.calendrier_debut.selectedDate()
        self.date_debut.setText(date_de_debut.toString("dd/MM/yyyy"))

        case = QTextCharFormat()
        case.setFontWeight(QFont.Bold)
        case.setBackground(QColor("#284856"))
        self.calendrier_debut.setDateTextFormat(date_de_debut, fmt)

    def actionneur_date_fin (self) : 
        date_de_fin = self.calendrier_fin.selectedDate()
        self.date_fin.setText(date_de_fin.toString("dd/MM/yyyy"))

        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold)
        fmt.setBackground(QColor("#284856"))
        self.calendrier_fin.setDateTextFormat(date_de_fin, fmt)

    # TODO: Regrouper les deux fonctions avec .sender()
        

