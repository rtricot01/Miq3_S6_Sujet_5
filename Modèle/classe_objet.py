from datetime import date
from Gestion_db import OptionsReservationPossibles,Session,ChambreDB,ReservationDB,add_to_db,add_to_db_room_option,add_to_db_reservation_option

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

    def __init__(self, reservation_id:int,room_id:int,client_id:int,start_date:date, end_date:date, spa, petit_dejeuner, parking, wifi):
        self.reservation_id=reservation_id
        self.room_id=room_id
        self.client_id=client_id
        self.start_date=start_date
        self.end_date=end_date
        self.spa=spa
        self.parking=parking
        self.petit_dejeuner=petit_dejeuner
        self.wifi=wifi




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
        return f"Chambre({self.room_id},{self.max_people},{self.price},{self.room_size})"

class OptionReservation:

    def __init__(self, reservation_id:int, option_reservation_id:OptionsReservationPossibles):
        self.reservation_id=reservation_id
        self.option_reservation_id=option_reservation_id

class OptionChambre:

    def __init__(self, room_id:int, option_chambre_id:OptionsReservationPossibles):
        self.room_id=room_id
        self.option_chambre_id=option_chambre_id


# def recuperer_chambre_libre(date_start:date, date_end:date, min_people:int=None) -> list[Chambre]:
#     """Cette fonction permet de récupérer une liste de chambre disponible pour une période donnée en argument et eventuellement un nombre de voyageur.
#     Cette fonction doit être appelé avec comme premier argument la date de début de reservation souhaitée et puis la date de fin souhaitée, tout deux de type 'date' en python, et le nombre de personne:int
#     (i.e. recuperer_chambre_libre(date(annee,mois,jour),date(annne,mois,jour), nbr_voyageur) """
#     room_id_list=[]
#     with Session() as session:
#         chambres = (session.query(ChambreDB).filter( 
#                     ~session.query(ReservationDB).filter(
#                                                   ReservationDB.room_id == ChambreDB.room_id,
#                                                   ReservationDB.start_date <= date_end,
#                                                   ReservationDB.end_date >=date_start,
#                                                   ).exists()))
        
#     if min_people is not None:
#         chambres=chambres.filter(ChambreDB.max_people>=min_people)

#     rows=chambres.all() 
#     for room in rows:
#         room_id_list.append(Chambre(room.room_id, room.max_people, room.prize, room.room_size, ))

#     return room_id_list


# print(recuperer_chambre_libre(date(2026,1,4),date(2026,1,8),3))


def creer_chambre(max_person:int, price:int, room_area:int, fumeur:bool, animaux_toleres:bool, climatisation:bool) -> Chambre:
    """Foncion qui permet de créer une instance chambre tout en l'enregistrant dans la base de donnée, et en remplissant le table liée aux options de chambre"""
    try:
        chambre=ChambreDB(max_people=max_person, prize=price, room_size=room_area)
        chambre=add_to_db(chambre)
        print(chambre.room_id)
        add_to_db_room_option(chambre.room_id,fumeur,animaux_toleres,climatisation)
        return Chambre(chambre.room_id, chambre.max_people, chambre.prize, chambre.room_size, fumeur, animaux_toleres, climatisation)
    #TODO Exception à changer
    except :
        raise 


def creer_reservation(id_room:int,id_client:int,date_start:date, date_end:date, spa:bool, petit_dejeuner:bool, parking:bool, wifi:bool):
    """Foncion qui permet de créer une instance de reservation tout en l'enregistrant dans la base de donnée, et en remplissant le table liée aux options de reservation"""
    try:
        reservation=ReservationDB(room_id=id_room, client_id=id_client, start_date=date_start, end_date=date_end)
        reservation=add_to_db(reservation)
        add_to_db_reservation_option(reservation.reservation_id, spa, petit_dejeuner, parking, wifi)
        return Reservation(reservation.reservation_id,id_room,id_client,date_start, date_end, spa, petit_dejeuner, parking, wifi)
    #TODO Exception à trouver
    except :
        raise



print(creer_chambre(5,80.99,40,True,False,True))
print(creer_reservation(13,1,date(2026,1,4),date(2026,1,8),True,False,True,False))




