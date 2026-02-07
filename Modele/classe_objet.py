from datetime import date
from Modele.gestion_db import Session,ChambreDB,ReservationDB,add_to_db
from Modele.exceptions import ReservationDateException



class Client:

    def __init__(self,client_id:int,client_firstname:str,client_lastname:str,client_tel:str,client_mail:str):
        self.client_id=client_id
        self.client_firstname=client_firstname
        self.client_lastname=client_lastname
        self.client_tel=client_tel
        self.client_mail=client_mail

    def __str__(self):
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
            


    def __str__(self):
        return f"Reservation({self.reservation_id},{self.room_id},{self.client_id},{self.nombre_personnes},{self.start_date},{self.end_date},{self.spa},{self.petit_dejeuner},{self.parking},{self.wifi})"



class Chambre:

    def __init__(self, room_id:int, max_people:int, price:int, room_size:int, fumeur:bool, animaux_toleres:bool, climatisation:bool):
        self.room_id=room_id
        self.max_people=max_people
        self.price=price
        self.room_size=room_size
        self.fumeur=fumeur
        self.animaux_toleres=animaux_toleres
        self.climatisation=climatisation


    def __repr__(self):
        return f"Chambre({self.room_id},{self.max_people},{self.price},{self.room_size},{self.fumeur},{self.animaux_toleres},{self.climatisation})"


def recuperer_chambre_libre(date_start:date, date_end:date, min_people:int=None, fumeur: bool = None, animaux_toleres: bool = None, climatisation: bool = None) -> list[Chambre]:
    """Cette fonction permet de récupérer une liste de chambres disponibles pour une période donnée en argument et eventuellement un nombre de voyageur.
     Cette fonction doit être appelé avec comme premier argument la date de début de reservation souhaitée et puis la date de fin souhaitée, tout deux de type 'date' en python, et le nombre de personne:int
     (i.e. recuperer_chambre_libre(date(annee,mois,jour),date(annne,mois,jour), nbr_voyageur) """
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

        rows=chambres.all() 
        for room in rows:
            room_list.append(Chambre(room.room_id, room.max_people, room.prize, room.room_size,room.fumeur, room.animaux_toleres, room.climatisation ))

    return room_list


def creer_chambre(max_person:int, price:int, room_area:int, fumeur:bool, animaux_toleres:bool, climatisation:bool) -> Chambre:
    """Fonction qui permet de créer une instance chambre tout en l'enregistrant dans la base de donnée"""
    try:
        chambre=ChambreDB(max_people=max_person, prize=price, room_size=room_area,fumeur=fumeur,animaux_toleres= animaux_toleres,climatisation=climatisation)
        chambre=add_to_db(chambre)
        print(chambre.room_id)
        return Chambre(chambre.room_id, chambre.max_people, chambre.prize, chambre.room_size, fumeur, animaux_toleres, climatisation)
    #TODO Exception à changer
    except :
        raise 


def creer_reservation(id_room:int,id_client:int,date_start:date, date_end:date, spa:bool, petit_dejeuner:bool, parking:bool, wifi:bool):
    """Foncion qui permet de créer une instance de reservation tout en l'enregistrant dans la base de donnée, et en remplissant le table liée aux options de reservation"""
    try:
        reservation=ReservationDB(room_id=id_room, client_id=id_client, start_date=date_start, end_date=date_end, spa = spa, petit_dejeuner =petit_dejeuner, parking= parking, wifi = wifi)
        reservation=add_to_db(reservation)
        return Reservation(reservation.reservation_id,id_room,id_client,date_start, date_end, spa, petit_dejeuner, parking, wifi)
    #TODO Exception à trouver
    except :
        raise

def toutes_les_reservations() -> list[Reservation]:
    """Fonction permettant d'afficher toutes les reservations de la BDD"""
    list_reservation =[]
    with Session() as session:
        reservations = session.query(ReservationDB).all()
    for reservation in reservations:
        list_reservation.append(Reservation(reservation.reservation_id, reservation.room_id, reservation.client_id, reservation.nombre_personnes, reservation.start_date, reservation.end_date, reservation.spa, reservation.petit_dejeuner, reservation.parking, reservation.wifi))
    return list_reservation   
       
print(recuperer_chambre_libre(date(2026,1,8), date(2026,1,8), 2, climatisation=True))



print(Reservation(1, 1, 1, 3, date(2026,2,2), date(2026,2,8), False, True, False, True))