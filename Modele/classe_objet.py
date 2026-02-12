from datetime import date
from Modele.gestion_db import session_db,ChambreDB,ReservationDB,ClientDB,add_to_db
from Modele.exceptions import ReservationDateException, ObjectNotFoundException
import logging
from tests.db_test import session_test

#TODO à mettre dans le 'main' du fichier qui va lancer l'application
from utils.logging_config import setup_logging 
setup_logging()



class Client:

    def __init__(self,client_id:int,client_firstname:str,client_lastname:str,client_tel:str,client_mail:str):
        self.client_id=client_id
        self.client_firstname=client_firstname
        self.client_lastname=client_lastname
        self.client_tel=client_tel
        self.client_mail=client_mail

    


    def __repr__(self):
        return f"Client({self.client_id},{self.client_firstname},{self.client_lastname},{self.client_tel},{self.client_mail})"

class Reservation:

    def __init__(self, reservation_id:int,room_id:int,client_id:int,nombre_personnes: int, start_date:date, end_date:date, spa: bool, petit_dejeuner: bool, parking: bool, wifi: bool):
        if start_date<end_date:
            self.reservation_id=reservation_id
            self.room_id=room_id
            self.client_id=client_id
            self.nombre_personnes = nombre_personnes
            self.start_date=start_date
            self.end_date=end_date
            self.spa=spa
            self.parking=parking
            self.petit_dejeuner=petit_dejeuner
            self.wifi=wifi
        else:
            raise ReservationDateException
            


    def __repr__(self):
        return f"Reservation({self.reservation_id},{self.room_id},{self.client_id},{self.nombre_personnes},{self.start_date},{self.end_date},{self.spa},{self.petit_dejeuner},{self.parking},{self.wifi})"



class Chambre:

    def __init__(self, room_id:int, max_people:int, price:float, room_size:int, fumeur:bool, animaux_toleres:bool, climatisation:bool):
        self.room_id=room_id
        self.max_people=max_people
        self.price=price
        self.room_size=room_size
        self.fumeur=fumeur
        self.animaux_toleres=animaux_toleres
        self.climatisation=climatisation


    def __repr__(self):
        return f"Chambre({self.room_id},{self.max_people},{self.price},{self.room_size},{self.fumeur},{self.animaux_toleres},{self.climatisation})"


def recuperer_chambre_libre_db(date_start:date, date_end:date, min_people:int, fumeur: bool, animaux_toleres: bool , climatisation: bool , price_min: float , price_max: float, Session = session_db) -> list[Chambre]:
    """Cette fonction permet de récupérer une liste de chambres disponibles pour une période donnée en argument et eventuellement un nombre de voyageur.
     Cette fonction doit être appelé avec comme premier argument la date de début de reservation souhaitée et puis la date de fin souhaitée, tout deux de type 'date' en python, et le nombre de personne:int
     (i.e. recuperer_chambre_libre(date(annee,mois,jour),date(annne,mois,jour), nbr_voyageur) """
    
    logging.info("START recuperer_chambre_libre")

    room_list=[]
    with Session() as session:
        chambres = (session.query(ChambreDB).filter( 
                     ~session.query(ReservationDB).filter(
                                                ReservationDB.room_id == ChambreDB.room_id,
                                                ReservationDB.start_date <= date_end,
                                                ReservationDB.end_date >=date_start,
                                                ).exists()))
        
        if min_people is not None:
            chambres=chambres.filter(ChambreDB.max_people>=min_people)
        if fumeur is not None:
            if fumeur is True:
                chambres=chambres.filter(ChambreDB.fumeur == True)
            else:
                chambres=chambres.filter(ChambreDB.fumeur == False)
        if animaux_toleres is not None:
            if animaux_toleres is True:
                chambres=chambres.filter(ChambreDB.animaux_toleres == True)
            else:
                chambres=chambres.filter(ChambreDB.animaux_toleres == False)
        if climatisation is not None:
            if climatisation is True:
                chambres=chambres.filter(ChambreDB.climatisation == True)
            else:
                chambres=chambres.filter(ChambreDB.climatisation == False)
        if price_min is not None:
            chambres=chambres.filter(ChambreDB.prize >= price_min)
        if price_max is not None:
            chambres=chambres.filter(ChambreDB.prize <= price_max)

        rows=chambres.all() 
        for room in rows:
            room_list.append(Chambre(room.room_id, room.max_people, room.prize, room.room_size,room.fumeur, room.animaux_toleres, room.climatisation ))
    logging.info(f"Récupération des chambres libres pour la période {date_start}/{date_end}")
    return room_list



def supprimer_reservation_db(id_reservation, Session = session_db):
    """Fonction permettant de supprimer une réservation à partir de son id"""
    try:
        with Session() as session:
            resa_a_supprimer = session.query(ReservationDB).filter(ReservationDB.reservation_id == id_reservation).first()
        if resa_a_supprimer:
                session.delete(resa_a_supprimer)
                session.commit()
                logging.info(f"Réservation {id_reservation} supprimée.")
        else:
                raise ObjectNotFoundException
    except Exception as e:
        raise e

def supprimer_chambre_db(id_chambre, Session = session_db):
    """Fonction permettant la suppression de la chambre ainsi que des réservations qui en dépendent à partir de son id"""
    try:
        with Session() as session:
            #Suppression des dépéendances de la chambre
            session.query(ReservationDB).filter(ReservationDB.room_id == id_chambre).delete()
            chambre_a_supprimer = session.query(ChambreDB).filter(ChambreDB.room_id == id_chambre).first()
            if chambre_a_supprimer:
                session.delete(chambre_a_supprimer)
                session.commit()
                logging.info(f"Chambre {id_chambre} supprimée.")
            else:
                raise ObjectNotFoundException
    except Exception as e:
        raise e

def supprimer_client_db(id_client, Session = session_db):
    """Fonction permettant la suppression d'un client ainsi que des réservations qui en dépendent à partir de son id"""
    try:
        with Session() as session:
            #Suppression des dépéendances du client
            session.query(ReservationDB).filter(ReservationDB.client_id == id_client).delete()
            client_a_supprimer = session.query(ClientDB).filter(ClientDB.client_id == id_client).first()
            if client_a_supprimer:
                session.delete(client_a_supprimer)
                session.commit()
                logging.info(f"Client {id_client} supprimé.")
            else:
                raise ObjectNotFoundException
    except Exception as e :
        raise e

def toutes_les_reservations(Session = session_db) -> list[Reservation]:
    """Fonction permettant d'afficher toutes les reservations de la BDD"""
    list_reservation =[]
    with Session() as session:
        reservations = session.query(ReservationDB).all()
    for reservation in reservations:
        list_reservation.append(Reservation(reservation.reservation_id, reservation.room_id, reservation.client_id, reservation.nombre_personnes, reservation.start_date, reservation.end_date, reservation.spa, reservation.petit_dejeuner, reservation.parking, reservation.wifi))
    logging.info(f"Recuperation de la liste des reservations.")
    return list_reservation   

def toutes_les_chambres(Session = session_db) -> list[Chambre]:
    """Fonction permettant d'afficher toutes les chambres de la BDD"""
    list_chambre =[]
    with Session() as session:
        chambres = session.query(ChambreDB).all()
    for chambre in chambres:
        list_chambre.append(Chambre(chambre.room_id, chambre.max_people, chambre.prize, chambre.room_size, chambre.fumeur, chambre.animaux_toleres, chambre.climatisation))
    logging.info(f"Recuperation de la liste des chambres.")
    return list_chambre

def tous_les_clients(Session = session_db) -> list[Client]:
    """Fonction permettant d'afficher tous les clients de la BDD"""
    list_client =[]
    with Session() as session:
        clients = session.query(ClientDB).all()
    for client in clients:
        list_client.append(Client(client.client_id ,client.client_firstname, client.client_lastname, client.client_tel, client.client_mail))
    logging.info(f"Recuperation de la liste des clients.")
    return list_client