from datetime import date
from src.hotel_manager.modele.gestion_db import session_db,ReservationDB,add_to_db
import logging
from src.hotel_manager.modele.classe_objet import Reservation, supprimer_reservation_db, toutes_les_reservations, modifier_reservation_db
from src.hotel_manager.controleur.controle_saisie import controler_max_personnes, controler_dates, controler_nombre_personnes


def creer_reservation(id_room:int,id_client:int, nombres_personnes:int, date_start:date, date_end:date, spa:bool, petit_dejeuner:bool, parking:bool, wifi:bool, Session = session_db) -> Reservation:
    """Foncion qui permet de créer une instance de reservation tout en l'enregistrant dans la base de donnée, et en remplissant le table liée aux options de reservation"""
    try:
        reservation=ReservationDB(room_id=id_room, client_id=id_client, nombre_personnes=nombres_personnes, start_date=date_start, end_date=date_end, spa = spa, petit_dejeuner =petit_dejeuner, parking= parking, wifi = wifi)
        reservation=add_to_db(reservation, Session)
        logging.info(f"Réservation cree, id:{reservation.reservation_id}")
        return Reservation(reservation.reservation_id,id_room,id_client, nombres_personnes, date_start, date_end, spa, petit_dejeuner, parking, wifi)
    except Exception as e:
        raise e

def suppression_reservation(id_reservation, Session = session_db) -> None:
    """Fonction qui permet de supprimer une réservation à partir de son id"""
    supprimer_reservation_db(id_reservation, Session)

def afficher_toutes_les_reservations(Session = session_db) -> list[Reservation]:
    """Fonction qui permet d'afficher toutes les réservations"""
    return toutes_les_reservations(Session)

def modifier_reservation(id_res: int, id_room: int, nombre_pers: int, date_debut: date, date_fin: date, spa: bool, petit_dej: bool, parking: bool, wifi: bool, Session = session_db):
    """Fonction qui met à jour les informations d'une réservation existante"""
    controler_dates(date_debut, date_fin, id_room, id_res, Session)
    controler_nombre_personnes(nombre_pers)
    controler_max_personnes(id_room, nombre_pers, Session)
    modifier_reservation_db(id_res, id_room, nombre_pers, date_debut, date_fin, spa, petit_dej, parking, wifi, Session)