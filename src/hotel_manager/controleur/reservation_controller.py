from datetime import date
from hotel_manager.modele.gestion_db import session_db,ReservationDB,add_to_db
import logging
from hotel_manager.modele.classe_objet import Reservation, supprimer_reservation_db, toutes_les_reservations


def creer_reservation(id_room:int,id_client:int, nombre_personnes:int, date_start:date, date_end:date, spa:bool, petit_dejeuner:bool, parking:bool, wifi:bool, Session = session_db) -> Reservation:
    """Foncion qui permet de créer une instance de reservation tout en l'enregistrant dans la base de donnée, et en remplissant le table liée aux options de reservation"""
    try:
        reservation=ReservationDB(room_id=id_room, client_id=id_client, nombre_personnes=nombre_personnes, start_date=date_start, end_date=date_end, spa = spa, petit_dejeuner =petit_dejeuner, parking= parking, wifi = wifi)
        reservation=add_to_db(reservation, Session)
        logging.info(f"Réservation cree, id:{reservation.reservation_id}")
        return Reservation(reservation.reservation_id,id_room,id_client, nombre_personnes, date_start, date_end, spa, petit_dejeuner, parking, wifi)
    except Exception as e:
        raise e

def suppression_reservation(id_reservation, Session = session_db) -> None:
    """Fonction qui permet de supprimer une réservation à partir de son id"""
    supprimer_reservation_db(id_reservation, Session)

def afficher_toutes_les_reservations(Session = session_db) -> list[Reservation]:
    """Fonction qui permet d'afficher toutes les réservations"""
    return toutes_les_reservations(Session)

