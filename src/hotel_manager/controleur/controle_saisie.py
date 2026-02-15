import re
from src.hotel_manager.modele.exceptions import TelephoneNumberException, EmailException, TooManyPeopleException, NotEnoughAdultsException, ReservationDateException
from init_db import session_db
from src.hotel_manager.modele.gestion_db import ChambreDB, ReservationDB
from datetime import date

EMAIL_REGEX= r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
ADULTES_MINIMUM = 1

def controler_telephone(telephone: str) -> bool:
    """Fonction permettant de controler le format du numero de telephone"""
    if (telephone.isdigit()):
        pass
    else:
        raise TelephoneNumberException

def controler_mail(mail: str) -> bool:
    """Fonction permettant de controler le format de l'adresse mail"""
    if re.match(EMAIL_REGEX, mail):
        pass
    else:
        raise EmailException

def controler_max_personnes(room_id : int, nombre_personnes: int, Session = session_db) -> None:
    """Fonction permettant de controler que le nombre de personnes d'une reservation est inferieur à la capacité de la chambre"""
    with Session() as session:
        chambre_db = session.query(ChambreDB).filter(ChambreDB.room_id == room_id).first()
        max_tolere = chambre_db.max_people
    if (nombre_personnes > max_tolere):
        raise TooManyPeopleException
    else:
        pass

def controler_dates(date_debut: date, date_fin: date, room_id:int, id_reservation_ignoree: int, Session = session_db) -> None:
    """Fonction permettant de controler que la chambre voulue est libre pendant les dates voulues"""
    with Session() as session:
        #On cherche ici un conflit possible avec une reservation existante sur les mêmes dates en ne prenant pas en compte la réservation à modifier
        conflit_possible = session.query(ReservationDB).filter(ReservationDB.room_id == room_id, ReservationDB.start_date < date_fin,
        ReservationDB.end_date > date_debut, ReservationDB.reservation_id != id_reservation_ignoree).first()
    if conflit_possible is None:
        pass
    else: 
        raise ReservationDateException

def controler_nombre_adultes(nombre_adultes: int) -> None:
    """Fonction permettant de controler qu'une reservatio, contient le nombre d'adultes minimum"""
    if nombre_adultes < ADULTES_MINIMUM:
        raise NotEnoughAdultsException
    else:
        pass