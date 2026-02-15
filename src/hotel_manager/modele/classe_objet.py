from datetime import date
from src.hotel_manager.modele.gestion_db import session_db,ChambreDB,ReservationDB,ClientDB
from src.hotel_manager.modele.exceptions import ReservationDateException, ObjectNotFoundException
import logging



class Client:

    def __init__(self,client_id:int,client_firstname:str,client_lastname:str,client_tel:str,client_mail:str):
        self.client_id=client_id
        self.client_firstname=client_firstname
        self.client_lastname=client_lastname
        self.client_tel=client_tel
        self.client_mail=client_mail

    
    def __eq__(self, other):
            if not isinstance(other, Client):
                return NotImplemented
        
            return (
                self.client_id==other.client_id and
                self.client_firstname==other.client_firstname and
                self.client_lastname== other.client_lastname and
                self.client_tel==other.client_tel and
                self.client_mail==other.client_mail
            )


    def __repr__(self) -> str:
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
            

    def __eq__(self, other):
        if not isinstance(other, Reservation):
            return NotImplemented
    
        return (
            self.reservation_id == other.reservation_id and
            self.room_id == other.room_id and
            self.client_id == other.client_id and
            self.nombre_personnes == other.nombre_personnes and
            self.start_date == other.start_date and
            self.end_date == other.end_date and
            self.spa == other.spa and
            self.petit_dejeuner == other.petit_dejeuner and
            self.parking == other.parking and
            self.wifi == other.wifi
            )

    def __repr__(self) -> str:
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


    def __repr__(self) -> str:
        return f"Chambre({self.room_id},{self.max_people},{self.price},{self.room_size},{self.fumeur},{self.animaux_toleres},{self.climatisation})"

    def __eq__(self, other):
        if not isinstance(other, Chambre):
            return NotImplemented
    
        return (
            self.room_id == other.room_id and
            self.max_people == other.max_people and
            self.price == other.price and
            self.room_size == other.room_size and
            self.fumeur == other.fumeur and
            self.animaux_toleres == other.animaux_toleres and
            self.climatisation == other.climatisation
    )


def recuperer_chambre_libre_db(date_start:date, date_end:date, min_people:int, fumeur: bool, animaux_toleres: bool , climatisation: bool , price_min: float , price_max: float, Session = session_db) -> list[Chambre]:     
    
    logging.info("START recuperer_chambre_libre")

    room_list = []
    with Session() as session:
        # Base de la requête : chambres qui n'ont pas de réservation sur ces dates
        chambres = (session.query(ChambreDB).filter( 
                    ~session.query(ReservationDB).filter(
                        ReservationDB.room_id == ChambreDB.room_id,
                        ReservationDB.start_date <= date_end,
                        ReservationDB.end_date >= date_start,
                    ).exists()))

        # --- FILTRES OBLIGATOIRES (Capacité et Prix) ---
        if min_people:
            chambres = chambres.filter(ChambreDB.max_people >= min_people)
        
        if price_min is not None:
            chambres = chambres.filter(ChambreDB.prize >= price_min)
        
        if price_max is not None:
            chambres = chambres.filter(ChambreDB.prize <= price_max)

        # --- FILTRES OPTIONS (Logique : "Si coché, alors obligatoire") ---
        # Si 'fumeur' est True, on ne veut QUE des chambres fumeurs.
        # Si 'fumeur' est False (décoché), on ne filtre pas du tout (on montre tout).
        if fumeur:
            chambres = chambres.filter(ChambreDB.fumeur.is_(True))
        
        if animaux_toleres:
            chambres = chambres.filter(ChambreDB.animaux_toleres.is_(True))
            
        if climatisation:
            chambres = chambres.filter(ChambreDB.climatisation.is_(True))

        rows = chambres.all() 
        for room in rows:
            room_list.append(Chambre(room.room_id, room.max_people, room.prize, room.room_size, room.fumeur, room.animaux_toleres, room.climatisation))
            
    logging.info(f"Récupération des chambres libres pour la période {date_start}/{date_end}")
    return room_list



def supprimer_reservation_db(id_reservation: int, Session = session_db) -> None:
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

def supprimer_chambre_db(id_chambre: int, Session = session_db) -> None:
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

def supprimer_client_db(id_client: int, Session = session_db) -> None:
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
    logging.info("Recuperation de la liste des reservations.")
    return list_reservation   

def toutes_les_chambres(Session = session_db) -> list[Chambre]:
    """Fonction permettant d'afficher toutes les chambres de la BDD"""
    list_chambre =[]
    with Session() as session:
        chambres = session.query(ChambreDB).all()
    for chambre in chambres:
        list_chambre.append(Chambre(chambre.room_id, chambre.max_people, chambre.prize, chambre.room_size, chambre.fumeur, chambre.animaux_toleres, chambre.climatisation))
    logging.info("Recuperation de la liste des chambres.")
    return list_chambre

def tous_les_clients(Session = session_db) -> list[Client]:
    """Fonction permettant d'afficher tous les clients de la BDD"""
    list_client =[]
    with Session() as session:
        clients = session.query(ClientDB).all()
    for client in clients:
        list_client.append(Client(client.client_id ,client.client_firstname, client.client_lastname, client.client_tel, client.client_mail))
    logging.info("Recuperation de la liste des clients.")
    return list_client