import pytest
from datetime import date 
from Modele.classe_objet import Client, Reservation, Chambre
from Modele.exceptions import ReservationDateException

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
