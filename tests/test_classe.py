import pytest
from datetime import date 
from src.hotel_manager.modele.classe_objet import Client, Reservation, Chambre
from src.hotel_manager.modele.exceptions import ReservationDateException, ObjectNotFoundException
from src.hotel_manager.controleur.chambre_controller import creer_chambre, suppression_chambre, afficher_toutes_les_chambres
from src.hotel_manager.controleur.reservation_controller import creer_reservation, suppression_reservation
from src.hotel_manager.controleur.client_controller import creer_client, suppression_client
from tests.db_test import sessiontest
from src.hotel_manager.modele.gestion_db import ChambreDB, ReservationDB, ClientDB




@pytest.mark.parametrize("id, firstname, lastname, tel, mail, expected_id, expected_firstname, expected_lastname, expected_tel, expected_mail",[
    (1, "Ahmet", "Tunc", "0607080910", "mail@mail.com", 1, "Ahmet", "Tunc", "0607080910", "mail@mail.com"),
    (1, "Jean Quentin", "Le Vêque", "+33607080910", "mail2@mail.fr",1, "Jean Quentin", "Le Vêque", "+33607080910", "mail2@mail.fr")
    ])
def test_constructeur_client(id: int, firstname: str, lastname:str, tel:str, mail:str, expected_id:int, expected_firstname:str, expected_lastname:str, expected_tel:str, expected_mail:str):
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
    with pytest.raises(ReservationDateException):
        Reservation(1, 1, 1, 1, date(2026,8,3), date(2026,8,1), True, False, False, True)




def test_constructeur_reservation_sans_option():
    with pytest.raises(TypeError):
        Reservation(1, 1, 1, 1, date(2026,8,3), date(2026,8,1))



@pytest.mark.parametrize("room_id, max_people, price, room_size, fumeur, animaux_toleres, climatisation, expected_room_id, " \
                         "expected_max_people, expected_price, expected_room_size, expected_fumeur, expected_animaux_toleres, " \
                         "expected_climatisation",[(1, 4, 89.99, 35, False, True, True,1, 4, 89.99, 35, False, True, True),
                                                  (12, 3, 75.99, 29, False, True, True, 12, 3, 75.99, 29, False, True, True)])
def test_constructeur_chambre(room_id:int, max_people:int, price:float, room_size:float, fumeur:bool, animaux_toleres:bool, climatisation:bool, 
                              expected_room_id:int,expected_max_people:int, expected_price:float, expected_room_size:float, expected_fumeur:bool, 
                              expected_animaux_toleres:bool,expected_climatisation:bool):
    chambre=Chambre(room_id, max_people, price, room_size, fumeur, animaux_toleres, climatisation)
    assert chambre.room_id==expected_room_id
    assert chambre.max_people==expected_max_people
    assert chambre.price==expected_price
    assert chambre.room_size==expected_room_size
    assert chambre.fumeur==expected_fumeur
    assert chambre.animaux_toleres==expected_animaux_toleres
    assert chambre.climatisation==expected_climatisation


def test_creer_chambre(sessiontest):
    chambre=creer_chambre(2,80.99,35,True, False,True,sessiontest)
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
        client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", sessiontest)
        with sessiontest() as session:
            client_db=session.get(ClientDB, client.client_id)
            assert client_db.client_id == client.client_id
            assert client_db.client_firstname == client.client_firstname
            assert client_db.client_lastname == client.client_lastname
            assert client_db.client_tel == client.client_tel
            assert client_db.client_mail == client.client_mail


def test_creer_reservation(sessiontest):
    chambre=creer_chambre(2,50.09,35,True, True,True,sessiontest)
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", sessiontest)
    reservation=creer_reservation(chambre.room_id,client.client_id,2,date(2026,1,8),date(2026,1,20),True, True, False, True, sessiontest)
    
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
    chambre=creer_chambre(2,80.99,35,True, False,True,sessiontest)
    chambre_2=creer_chambre(2,80.99,35,True, False,True,sessiontest)
    with sessiontest() as session:
        chambre_db=session.get(ChambreDB,chambre.room_id)
        chambre_2_db=session.get(ChambreDB,chambre_2.room_id)
        assert chambre_db != None
        assert chambre_2_db != None

    suppression_chambre(chambre.room_id,sessiontest)

    with sessiontest() as session:
        chambre_db=session.get(ChambreDB, chambre.room_id)
        chambre_2_db=session.get(ChambreDB, chambre_2.room_id)
        assert chambre_db == None
        assert chambre_2_db != None



def test_suppression_reservation(sessiontest):
    chambre=creer_chambre(2,50.09,35,True, True,True,sessiontest)
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", sessiontest)
    reservation=creer_reservation(chambre.room_id,client.client_id,2,date(2026,1,8),date(2026,1,20),True, True, False, True, sessiontest)
    reservation_2=creer_reservation(chambre.room_id,client.client_id,2,date(2026,1,8),date(2026,1,20),True, True, False, True, sessiontest)
    with sessiontest() as session:
        reservation_db=session.get(ReservationDB, reservation.reservation_id)
        reservation_2_db=session.get(ReservationDB, reservation_2.reservation_id)
        assert reservation_db != None 
        assert reservation_2_db != None
        

    suppression_reservation(reservation.reservation_id, sessiontest)

    with sessiontest() as session:
        reservation_db=session.get(ReservationDB, reservation.reservation_id)
        reservation_2_db=session.get(ReservationDB, reservation_2.reservation_id)
        assert reservation_db == None
        assert reservation_2_db != None



def test_suppression_client(sessiontest):
    client=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", sessiontest)
    client_2=creer_client("Ahmet", "TUNC", "0102030405", "ahmet.tunc@insa-strasbourg.fr", sessiontest)

    with sessiontest() as session:
        client_db=session.get(ClientDB, client.client_id)
        client_2_db=session.get(ClientDB, client_2.client_id)
        assert client_db != None
        assert client_2_db != None

    suppression_client(client.client_id, sessiontest)

    with sessiontest() as session:
        client_db=session.get(ClientDB, client.client_id)
        client_2_db=session.get(ClientDB, client_2.client_id)
        assert client_db == None
        assert client_2_db != None

    
def test_suppression_chambre_id_incorrect(sessiontest):
    with pytest.raises(ObjectNotFoundException):
        suppression_chambre(10,sessiontest)

def test_suppression_reservation_id_incorrect(sessiontest):
    with pytest.raises(ObjectNotFoundException):
        suppression_reservation(10,sessiontest)

def test_suppression_client_id_incorrect(sessiontest):
    with pytest.raises(ObjectNotFoundException):
        suppression_client(10,sessiontest)

def test_recuperer_toutes_les_chambres(sessiontest):
    chambres=[]
    chambres.append(creer_chambre(2,50.09,35,True, True,True,sessiontest))
    chambres.append(creer_chambre(3,60.99,45,True, False,True,sessiontest))
    chambres.append(creer_chambre(4,70.99,35,False, False,True,sessiontest))
    chambres.append(creer_chambre(5,80.99,60,True, True,True,sessiontest))
    chambres.append(creer_chambre(6,90.99,35,True, False,True,sessiontest))
    chambres_db=afficher_toutes_les_chambres(sessiontest)
    assert len(chambres_db)==len(chambres)
    for chambre_db, chambre in zip(chambres_db,chambres):
        assert chambre_db.room_id ==chambre.room_id
        assert chambre_db.max_people == chambre.max_people
        assert chambre_db.price == chambre.price
        assert chambre_db.room_size == chambre.room_size
        assert chambre_db.fumeur == chambre.fumeur
        assert chambre_db.animaux_toleres == chambre.animaux_toleres
        assert chambre_db.climatisation == chambre.climatisation






    

# def test_recuperer_chambres_libres(sessiontest):
#     chambres=[]
#     chambres.append(creer_chambre(2,50.09,35,True, True,True,sessiontest))
#     chambres.append(creer_chambre(3,60.99,45,True, False,True,sessiontest))
#     chambres.append(creer_chambre(4,70.99,35,False, False,True,sessiontest))
#     chambres.append(creer_chambre(5,80.99,60,True, True,True,sessiontest))
#     chambres.append(creer_chambre(6,90.99,35,True, False,True,sessiontest))

#     reservation=[]
#     pass