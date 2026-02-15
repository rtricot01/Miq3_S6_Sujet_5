from src.hotel_manager.modele.gestion_db import session_db,ChambreDB,add_to_db
import logging
from src.hotel_manager.modele.classe_objet import Chambre, supprimer_chambre_db, toutes_les_chambres, recuperer_chambre_libre_db


def creer_chambre(max_person:int, price:float, room_area:int, fumeur:bool, animaux_toleres:bool, climatisation:bool, Session = session_db) -> Chambre:
    """Fonction qui permet de créer une instance chambre tout en l'enregistrant dans la base de donnée"""
    try:
        chambre=ChambreDB(max_people=max_person, prize=price, room_size=room_area,fumeur=fumeur,animaux_toleres= animaux_toleres,climatisation=climatisation)
        chambre=add_to_db(chambre, Session)
        logging.info(f"Chambre cree, id:{chambre.room_id}")
        return Chambre(chambre.room_id, chambre.max_people, chambre.prize, chambre.room_size, fumeur, animaux_toleres, climatisation)
    #TODO Exception à changer
    except :
        raise 

def suppression_chambre(id_chambre, Session = session_db) -> None:
    """Fonction permettant de supprimer une chambre à partir de son id"""
    return supprimer_chambre_db(id_chambre, Session)

def afficher_toutes_les_chambres(Session=session_db) -> list[Chambre]:
    """Fonction permettant d'afficher toutes les chambres"""
    return toutes_les_chambres(Session)

def recuperer_chambre_libre(date_start, date_end, min_people=None, fumeur= None, animaux_toleres = None, climatisation = None, price_min= None, price_max = None, Session = session_db) -> list[Chambre]:
    """Fonction permettant de récupérer les chambres libres selon les critères d'options et les dates"""
    return recuperer_chambre_libre_db(date_start, date_end, min_people, fumeur, animaux_toleres, climatisation, price_min, price_max, Session)
