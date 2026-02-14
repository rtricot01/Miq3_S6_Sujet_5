import pytest
from datetime import date 
from src.hotel_manager.modele.classe_objet import Client, Reservation, Chambre
from src.hotel_manager.modele.exceptions import ReservationDateException, ObjectNotFoundException, EmailException, TelephoneNumberException
from src.hotel_manager.controleur.chambre_controller import creer_chambre, suppression_chambre, afficher_toutes_les_chambres, recuperer_chambre_libre
from src.hotel_manager.controleur.reservation_controller import creer_reservation, suppression_reservation, afficher_toutes_les_reservations, modifier_reservation
from src.hotel_manager.controleur.client_controller import creer_client, suppression_client, afficher_tous_les_clients
from tests.db_test import sessiontest
from src.hotel_manager.modele.gestion_db import ChambreDB, ReservationDB, ClientDB




@pytest.mark.parametrize("id, firstname, lastname, tel, mail, expected_id, expected_firstname, expected_lastname, expected_tel, expected_mail",[
    (1, "Ahmet", "Tunc", "0607080910", "mail@mail.com", 1, "Ahmet", "Tunc", "0607080910", "mail@mail.com"),
    (1, "Jean Quentin", "Le Vêque", "+33607080910", "mail2@mail.fr",1, "Jean Quentin", "Le Vêque", "+33607080910", "mail2@mail.fr")
    ])
def test_constructeur_client(id: int, firstname: str, lastname:str, tel:str, mail:str, expected_id:int, expected_firstname:str, expected_lastname:str, expected_tel:str, expected_mail:str):
    """Fonction qui teste la méthode constructeur de la classe client"""
    client = Client(id, firstname, lastname, tel, mail)
    assert client.client_id == expected_id
    assert client.client_firstname == expected_firstname
    assert client.client_lastname == expected_lastname
    assert client.client_tel == expected_tel
    assert client.client_mail == expected_mail
    




@pytest.mark.parametrize("id, room_id, client_id, nombre_personnes, start_date, end_date, spa, petit_dejeuner, parking, wifi, " \
                         "expected_id, expected_room_id, expected_client_id, expected_nombre_personnes, expected_start_date, " \
                         "expected_end_date, expected_spa, expected_petit_dejeuner, expected_parking, expected_wifi",[
                         (1, 1, 1, 3, date(2026,1,8), date(2026,1,15), False, True, False, False, 1, 1, 1, 3, date(2026,1,8), date(2026,1,15), False, True, False, False),
                         (2, 3, 2, 3, date(2027,1,8), date(2027,3,15), False, True, False, False, 2, 3, 2, 3, date(2027,1,8), date(2027,3,15), False, True, False, False)
                         ])
def test_constructeur_reservation(id:int, room_id:int, client_id:int, nombre_personnes:int, start_date:date, end_date:date, spa:bool, petit_dejeuner:bool, parking:bool, wifi:bool,
                                  expected_id:int, expected_room_id:int, expected_client_id:int, expected_nombre_personnes:int, expected_start_date:date,
                                  expected_end_date:date, expected_spa:bool, expected_petit_dejeuner:bool, expected_parking:bool, expected_wifi:bool):
    """Fonction qui teste la méthode constructeur de la classe Reservation"""

    reservation=Reservation(id, room_id, client_id, nombre_personnes, start_date, end_date, spa, petit_dejeuner, parking, wifi)
    assert reservation.reservation_id==expected_id
    assert reservation.room_id==expected_room_id
    assert reservation.client_id==expected_client_id
    assert reservation.nombre_personnes==expected_nombre_personnes
    assert reservation.start_date==expected_start_date
    assert reservation.end_date==expected_end_date
    assert reservation.spa==expected_spa
    assert reservation.petit_dejeuner==expected_petit_dejeuner
    assert reservation.parking==expected_parking
    assert reservation.wifi==expected_wifi





def test_constructeur_reservation_date():
    """Fonction qui teste que ReservationDateException soit bien levé lorsque la chronologie des dates saisies n'est pas cohérente."""
    with pytest.raises(ReservationDateException):
        Reservation(1, 1, 1, 1, date(2026,8,3), date(2026,8,1), True, False, False, True)




def test_constructeur_reservation_sans_option():
    """Fonction qui teste que TypeError soit bien levé lorsqu'il manque les options dans le constructeur de Reservation"""
    with pytest.raises(TypeError):
        Reservation(1, 1, 1, 1, date(2026,8,3), date(2026,8,1))



@pytest.mark.parametrize("room_id, max_people, price, room_size, fumeur, animaux_toleres, climatisation, expected_room_id, " \
                         "expected_max_people, expected_price, expected_room_size, expected_fumeur, expected_animaux_toleres, " \
                         "expected_climatisation",[(1, 4, 89.99, 35, False, True, True,1, 4, 89.99, 35, False, True, True),
                                                  (12, 3, 75.99, 29, False, True, True, 12, 3, 75.99, 29, False, True, True)])
def test_constructeur_chambre(room_id:int, max_people:int, price:float, room_size:float, fumeur:bool, animaux_toleres:bool, climatisation:bool, 
                              expected_room_id:int,expected_max_people:int, expected_price:float, expected_room_size:float, expected_fumeur:bool, 
                              expected_animaux_toleres:bool,expected_climatisation:bool):
    """Fonction qui teste la méthode constructeur de la classe Chambre"""

    chambre=Chambre(room_id, max_people, price, room_size, fumeur, animaux_toleres, climatisation)
    assert chambre.room_id==expected_room_id
    assert chambre.max_people==expected_max_people
    assert chambre.price==expected_price
    assert chambre.room_size==expected_room_size
    assert chambre.fumeur==expected_fumeur
    assert chambre.animaux_toleres==expected_animaux_toleres
    assert chambre.climatisation==expected_climatisation


def test_creer_chambre(sessiontest):
    """Fonction qui teste la fonction de création de chambre qui créer l'objet et le sauvgardedans la base de donnée. 
    Le test compare l'instance de chambre créée par la fonction 'creer_chambre' et l'instance de chambre créée en récuperant l'objet dans la base de donnée"""
    chambre=creer_chambre(2,80.99,35,True, False,True,Session=sessiontest)
    assert chambre.room_id is not None
    assert chambre.max_people == 2
    assert chambre.price == 80.99
    assert chambre.room_size == 35
    assert chambre.fumeur is True
    assert chambre.animaux_toleres is False
    assert chambre.climatisation is True

    with sessiontest() as session:
        chambre_db=session.get(ChambreDB,chambre.room_id)
        assert chambre_db.room_id is not None
        assert chambre_db.max_people == 2
        assert chambre_db.prize == 80.99
        assert chambre_db.room_size == 35
        assert chambre_db.fumeur is True
        assert chambre_db.animaux_toleres is False
        assert chambre_db.climatisation is True


def test_creer_client(sessiontest):
    """Fonction qui teste la fonction de création de client qui créer l'objet et le sauvgardedans la base de donnée. 
    Le test compare l'instance de client créée par la fonction 'creer_client' et l'instance de client créée en récuperant l'objet dans la base de donnée"""
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    with sessiontest() as session:
        client_db=session.get(ClientDB, client.client_id)
        assert client_db.client_id == client.client_id
        assert client_db.client_firstname == client.client_firstname
        assert client_db.client_lastname == client.client_lastname
        assert client_db.client_tel == client.client_tel
        assert client_db.client_mail == client.client_mail


@pytest.mark.parametrize("mail",[("ahmet.tunc@insa-strasbourgfr"),
                                 ("@insa-strasbourg.fr"),
                                 ("ahmet.tunc @insa-strasbourg.fr"),
                                 ("ahmet.tuncainsa-strasbourg.fr")])
def test_creer_client_erreur_mail(mail,sessiontest):
    """Fonction qui teste que EmailException soit bien levé lorsque le mail est mal saisie lors de la création d'un client."""
    with pytest.raises(EmailException):
        client=creer_client("Ahmet", "TUNC", "0102030405", mail, Session=sessiontest)

@pytest.mark.parametrize("tel",[("O123456789"),("012345678 9")])
def test_creer_client_erreur_tel(tel,sessiontest):
    """Fonction qui teste que TelephoneNumberException soit bien levé lorsque le numéro de téléphone est mal saisie lors de la création d'un client."""
    with pytest.raises(TelephoneNumberException):
        client=creer_client("Ahmet", "TUNC", tel, "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)

def test_creer_reservation(sessiontest):
    """Fonction qui teste la fonction de création de reservation qui créer l'objet et le sauvgardedans la base de donnée. 
    Le test compare l'instance de reservation créée par la fonction 'creer_reservation' et l'instance de reservation créée en récuperant l'objet dans la base de donnée"""
    chambre=creer_chambre(2,50.09,35,True, True,True,Session=sessiontest)
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    reservation=creer_reservation(chambre.room_id,client.client_id,2,date(2026,1,8),date(2026,1,20),True, True, False, True, Session=sessiontest)
    
    with sessiontest() as session:
        reservation_db=session.get(ReservationDB, reservation.reservation_id)
        assert reservation_db is not None
        assert reservation_db.reservation_id == reservation.reservation_id
        assert reservation_db.room_id == reservation.room_id
        assert reservation_db.client_id == reservation.client_id
        assert reservation_db.nombre_personnes == reservation.nombre_personnes
        assert reservation_db.start_date == reservation.start_date
        assert reservation_db.end_date == reservation.end_date
        assert reservation_db.spa == reservation.spa
        assert reservation_db.petit_dejeuner == reservation.petit_dejeuner
        assert reservation_db.parking == reservation.parking
        assert reservation_db.wifi == reservation.wifi


def test_suppression_chambre(sessiontest):
    """Fonction qui teste la suppression d'un objet chambre en base de donnée, en le créant, en verifiant sa présence, 
    puis en vérifiant que l'objet n'existe plus en base de donnée, après l'avoir supprimé avec la méthode 'suppression_chambre'."""
    chambre=creer_chambre(2,80.99,35,True, False,True,Session=sessiontest)
    chambre_2=creer_chambre(2,80.99,35,True, False,True,Session=sessiontest)
    with sessiontest() as session:
        chambre_db=session.get(ChambreDB,chambre.room_id)
        chambre_2_db=session.get(ChambreDB,chambre_2.room_id)
        assert chambre_db != None
        assert chambre_2_db != None

    suppression_chambre(chambre.room_id,Session=sessiontest)

    with sessiontest() as session:
        chambre_db=session.get(ChambreDB, chambre.room_id)
        chambre_2_db=session.get(ChambreDB, chambre_2.room_id)
        assert chambre_db == None
        assert chambre_2_db != None



def test_suppression_reservation(sessiontest):
    """Fonction qui teste la suppression d'un objet reservation en base de donnée, en le créant, en verifiant sa présence, 
    puis en vérifiant que l'objet n'existe plus en base de donnée, après l'avoir supprimé avec la méthode 'suppression_reservation'."""
    chambre=creer_chambre(2,50.09,35,True, True,True,Session=sessiontest)
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    reservation=creer_reservation(chambre.room_id,client.client_id,2,date(2026,1,8),date(2026,1,20),True, True, False, True, Session=sessiontest)
    reservation_2=creer_reservation(chambre.room_id,client.client_id,2,date(2026,1,8),date(2026,1,20),True, True, False, True, Session=sessiontest)
    with sessiontest() as session:
        reservation_db=session.get(ReservationDB, reservation.reservation_id)
        reservation_2_db=session.get(ReservationDB, reservation_2.reservation_id)
        assert reservation_db != None 
        assert reservation_2_db != None
        

    suppression_reservation(reservation.reservation_id, Session=sessiontest)

    with sessiontest() as session:
        reservation_db=session.get(ReservationDB, reservation.reservation_id)
        reservation_2_db=session.get(ReservationDB, reservation_2.reservation_id)
        assert reservation_db == None
        assert reservation_2_db != None



def test_suppression_client(sessiontest):
    """Fonction qui teste la suppression d'un objet client en base de donnée, en le créant, en verifiant sa présence, 
    puis en vérifiant que l'objet n'existe plus en base de donnée, après l'avoir supprimé avec la méthode 'suppression_client'."""
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    client_2=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)

    with sessiontest() as session:
        client_db=session.get(ClientDB, client.client_id)
        client_2_db=session.get(ClientDB, client_2.client_id)
        assert client_db != None
        assert client_2_db != None

    suppression_client(client.client_id, Session=sessiontest)

    with sessiontest() as session:
        client_db=session.get(ClientDB, client.client_id)
        client_2_db=session.get(ClientDB, client_2.client_id)
        assert client_db == None
        assert client_2_db != None

    
def test_suppression_chambre_id_incorrect(sessiontest):
    """Fonction qui teste que l'exception ObjectNotFoundException soit bien levé lorsque l'on essaye de supprimer un objet inexistant en base de donnée. """
    with pytest.raises(ObjectNotFoundException):
        suppression_chambre(10,Session=sessiontest)

def test_suppression_reservation_id_incorrect(sessiontest):
    """Fonction qui teste que l'exception ObjectNotFoundException soit bien levé lorsque l'on essaye de supprimer un objet inexistant en base de donnée. """
    with pytest.raises(ObjectNotFoundException):
        suppression_reservation(10,Session=sessiontest)

def test_suppression_client_id_incorrect(sessiontest):
    """Fonction qui teste que l'exception ObjectNotFoundException soit bien levé lorsque l'on essaye de supprimer un objet inexistant en base de donnée. """
    with pytest.raises(ObjectNotFoundException):
        suppression_client(10,Session=sessiontest)

def test_recuperer_toutes_les_chambres(sessiontest):
    """Fonction qui teste la récupération des chambres dans la base de donnée. Des chambres sont créer dans la base de donnée à l'aide de la fonction 'creer_chambre',
    puis avec la méthode 'afficher_toutes_les_chambres' on récupère toutes les chambres de la base de donnée dans une liste. Le test est validé si la liste de 
    chambre issue de la base de donnée et la liste de chambre créée sont les mêmes"""
    chambres=[]
    chambres.append(creer_chambre(2,50.09,35,True, True,True,Session=sessiontest))
    chambres.append(creer_chambre(3,60.99,45,True, False,True,Session=sessiontest))
    chambres.append(creer_chambre(4,70.99,35,False, False,True,Session=sessiontest))
    chambres.append(creer_chambre(5,80.99,60,True, True,True,Session=sessiontest))
    chambres.append(creer_chambre(6,90.99,35,True, False,True,Session=sessiontest))
    chambres_db=afficher_toutes_les_chambres(Session=sessiontest)
    chambres_db.sort(key=lambda c: c.room_id)
    assert len(chambres_db)==len(chambres)
    assert chambres == chambres_db

def test_recuperer_chambres_libres(sessiontest):
    """Fonction qui teste la récupération des chambres libres en donnant des dates de réservation, un nombre de voyageur, et d'autres attributs facultatifs. 
    Des réservations initiales sont créer et en appelant la fonction 'recuperer_chambre_libre' pour un certaine période, on vérifie que les chambres récupéré 
    de la base de donnée soit bien celle qui n'ont pas de réservation pour cette période . """
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    chambre=creer_chambre(2,50.09,35,True, False,True,Session=sessiontest)
    chambre_2=creer_chambre(3,60.99,45,True, False,True,Session=sessiontest)
    chambre_3=creer_chambre(4,70.99,35,False, False,True,Session=sessiontest)
    chambre_4=creer_chambre(5,80.99,60,True, True,True,Session=sessiontest)
    chambre_5=creer_chambre(6,90.99,35,True, False,True,Session=sessiontest)
    reservation=creer_reservation(chambre.room_id,client.client_id,2,date(2026,9,1),date(2026,9,7),True, True, False, True, Session=sessiontest)
    reservation_2=creer_reservation(chambre_2.room_id,client.client_id,2,date(2026,9,8),date(2026,9,20),True, True, False, True, Session=sessiontest)
    reservation_3=creer_reservation(chambre_3.room_id,client.client_id,2,date(2026,9,14),date(2026,11,15),True, True, False, True, Session=sessiontest)
    reservation_4=creer_reservation(chambre_4.room_id,client.client_id,2,date(2026,11,23),date(2026,12,10),True, True, False, True, Session=sessiontest)
    reservation_5=creer_reservation(chambre_5.room_id,client.client_id,2,date(2026,12,3),date(2026,12,10),True, True, False, True, Session=sessiontest)

    chambres_libres_2_personnes=recuperer_chambre_libre(date(2026,9,8), date(2026,11,29), 2,Session=sessiontest)
    chambres_libres_4_personnes=recuperer_chambre_libre(date(2026,9,8), date(2026,11,29), 4,Session=sessiontest)
    
    assert len(chambres_libres_2_personnes) == 2
    assert len(chambres_libres_4_personnes) == 1

    assert chambre in chambres_libres_2_personnes 
    assert chambre_5 in chambres_libres_2_personnes
    assert chambre_2 not in chambres_libres_2_personnes 
    assert chambre_3 not in chambres_libres_2_personnes 
    assert chambre_4 not in chambres_libres_2_personnes 
    assert chambre_5 in chambres_libres_4_personnes 
    assert chambre not in chambres_libres_4_personnes 
    assert chambre_2 not in chambres_libres_4_personnes 
    assert chambre_3 not in chambres_libres_4_personnes 
    assert chambre_4 not in chambres_libres_4_personnes 


def test_recuperer_toutes_les_reservations(sessiontest):
    """Fonction qui teste la récupération des reservations dans la base de donnée. Des reservations sont créer dans la base de donnée à l'aide de la fonction 'creer_reservation',
    puis avec la méthode 'afficher_toutes_les_reservations' on récupère toutes les reservations de la base de donnée dans une liste. Le test est validé si la liste de 
    reservation issue de la base de donnée et la liste de reservation créée sont les mêmes"""
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    chambre=creer_chambre(2,50.09,35,True, False,True,Session=sessiontest)
    chambre_2=creer_chambre(3,60.99,45,True, False,True,Session=sessiontest)
    chambre_3=creer_chambre(4,70.99,35,False, False,True,Session=sessiontest)
    chambre_4=creer_chambre(5,80.99,60,True, True,True,Session=sessiontest)
    chambre_5=creer_chambre(6,90.99,35,True, False,True,Session=sessiontest)
    reservations=[]
    reservations.append(creer_reservation(chambre.room_id,client.client_id,2,date(2026,9,1),date(2026,9,7),True, True, False, True, Session=sessiontest))
    reservations.append(creer_reservation(chambre_2.room_id,client.client_id,2,date(2026,9,8),date(2026,9,20),True, True, False, True, Session=sessiontest))
    reservations.append(creer_reservation(chambre_3.room_id,client.client_id,2,date(2026,9,14),date(2026,11,15),True, True, False, True, Session=sessiontest))
    reservations.append(creer_reservation(chambre_4.room_id,client.client_id,2,date(2026,11,23),date(2026,12,10),True, True, False, True, Session=sessiontest))
    reservations.append(creer_reservation(chambre_5.room_id,client.client_id,2,date(2026,12,3),date(2026,12,10),True, True, False, True, Session=sessiontest))

    reservations_db=afficher_toutes_les_reservations(Session=sessiontest)
    reservations_db.sort(key=lambda r: r.reservation_id)
    assert reservations_db == reservations
    

def test_recuperer_tous_les_clients(sessiontest):
    """Fonction qui teste la récupération des clients dans la base de donnée. Des clients sont créer dans la base de donnée à l'aide de la fonction 'creer_client',
    puis avec la méthode 'afficher_tous_les_clients' on récupère toutes les clients de la base de donnée dans une liste. Le test est validé si la liste de 
    client issue de la base de donnée et la liste de client créée sont les mêmes"""
    client=[]
    client.append(creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest))
    client.append(creer_client("Quentin", "LEVEQUE", "0102060405", "quentin.leveque@insa-strasbourg.fr", Session=sessiontest))
    client.append(creer_client("Louane", "SIALELLI", "0104530405", "louane.sialelli@insa-strasbourg.fr", Session=sessiontest))
    client.append(creer_client("Raphael", "TRICOT", "0102310405", "raphael.tricot@insa-strasbourg.fr", Session=sessiontest))

    clients_db=afficher_tous_les_clients(Session=sessiontest)
    clients_db.sort(key=lambda c: c.client_id)
    assert clients_db==client


@pytest.mark.parametrize("c1, c2, expected", [(Chambre(1, 2, 80.99, 35, True, False, True),Chambre(1, 2, 80.99, 35, True, False, True),True),
                                                (Chambre(1, 2, 80.99, 35, True, False, True),Chambre(2, 2, 80.99, 35, True, False, True),False),
                                                (Chambre(1, 2, 80.99, 35, True, False, True),Chambre(1, 3, 80.99, 35, True, False, True),False),
                                                (Chambre(1, 2, 80.99, 35, True, False, True),Chambre(1, 2, 90.99, 35, True, False, True),False)])
def test_egalite_chambre(c1, c2, expected):
    """Fonction qui teste la méthode de classe '__eq__' pour la classe Chambre."""
    assert (c1 == c2) == expected



@pytest.mark.parametrize("cl1, cl2, expected", [(Client(1, "Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr"),Client(1, "Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr"),True),
                                                (Client(1, "Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr"),Client(2, "Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr"),False),
                                                (Client(1, "Ahmet", "TUNC", "0102030405", "ahmet@insa.fr"),Client(1, "Amhet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr"),False),
                                                (Client(1, "Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr"),Client(1, "Ahmet", "TUNC", "0", "ahmet.tunc@insa-strasbourg.fr"),False)])
def test_egalite_client(cl1, cl2, expected):
    """Fonction qui teste la méthode de classe '__eq__' pour la classe Client."""
    assert (cl1 == cl2) == expected


@pytest.mark.parametrize("r1, r2, expected", [(Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),
                                                Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),True),
                                                (Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),
                                                Reservation(2, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),False),
                                                (Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),
                                                Reservation(1, 2, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),False),
                                                (Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),
                                                Reservation(1, 1, 1, 3, date(2026,9,1), date(2026,9,7), True, True, False, True),False),
                                                (Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),
                                                Reservation(1, 1, 1, 2, date(2026,9,2), date(2026,9,7), True, True, False, True),False),
                                                (Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), True, True, False, True),
                                                Reservation(1, 1, 1, 2, date(2026,9,1), date(2026,9,7), False, True, False, True),False) ])
def test_egalite_reservation(r1, r2, expected):
    """Fonction qui teste la méthode de classe '__eq__' pour la classe Reservation."""

    assert (r1 == r2) == expected

def test_modifier_reservation(sessiontest):
    """Fonction qui teste la modification de reservation en vérifiant le changement des attributs de l'objet stocké en base de donnée"""
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", Session=sessiontest)
    chambre=creer_chambre(2,50.09,35,True, False,True,Session=sessiontest)
    reservation=creer_reservation(chambre.room_id,client.client_id,2,date(2026,9,1),date(2026,9,7),True, True, False, True, Session=sessiontest)

    with sessiontest() as session:
        reservation_db=session.get(ReservationDB,reservation.reservation_id)
        assert reservation_db.reservation_id == reservation.reservation_id
        assert reservation_db.room_id == reservation.room_id
        assert reservation_db.client_id == reservation.client_id
        assert reservation_db.nombre_personnes == reservation.nombre_personnes
        assert reservation_db.start_date == reservation.start_date
        assert reservation_db.end_date == reservation.end_date
        assert reservation_db.spa == reservation.spa
        assert reservation_db.petit_dejeuner == reservation.petit_dejeuner
        assert reservation_db.parking == reservation.parking
        assert reservation_db.wifi == reservation.wifi

    modifier_reservation(reservation.reservation_id,chambre.room_id, 1, date(2026,9,4), date(2026,9,15), False, True, False, True, Session=sessiontest)

    with sessiontest() as session:
        reservation_db=session.get(ReservationDB,reservation.reservation_id)
        assert reservation_db.reservation_id == reservation.reservation_id
        assert reservation_db.room_id == reservation.room_id
        assert reservation_db.client_id == reservation.client_id
        assert reservation_db.nombre_personnes == 1
        assert reservation_db.start_date == date(2026,9,4)
        assert reservation_db.end_date == date(2026,9,15)
        assert reservation_db.spa == False
        assert reservation_db.petit_dejeuner == reservation.petit_dejeuner
        assert reservation_db.parking == reservation.parking
        assert reservation_db.wifi == reservation.wifi

    