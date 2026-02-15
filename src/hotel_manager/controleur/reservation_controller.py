from datetime import date
from hotel_manager.modele.gestion_db import session_db,ReservationDB,add_to_db
import logging
from hotel_manager.modele.classe_objet import Reservation, supprimer_reservation_db, toutes_les_reservations


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

def modifier_reservation(id_res, id_room, nombre_pers, date_start, date_end, spa, petit_dej, parking, wifi, Session = session_db):
    """Fonction qui met à jour les informations d'une réservation existante"""
    with Session() as session:
        res_db = session.query(ReservationDB).filter(ReservationDB.reservation_id == id_res).first()
        if res_db:
            res_db.room_id = id_room
            res_db.nombre_personnes = nombre_pers
            res_db.start_date = date_start
            res_db.end_date = date_end
            res_db.spa = spa
            res_db.petit_dejeuner = petit_dej
            res_db.parking = parking
            res_db.wifi = wifi
            session.commit()
            logging.info(f"Réservation {id_res} mise à jour.")
        else:
            raise Exception("Réservation non trouvée")