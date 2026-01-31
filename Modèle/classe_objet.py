from datetime import date
from Gestion_db import OptionsPossibles

class Client:

    def __init__(self,client_id:int,client_firstname:str,client_lastname:str,client_tel:str,client_mail:str):
        self.client_id=client_id
        self.client_firstname=client_firstname
        self.client_lastname=client_lastname
        self.client_tel=client_tel
        self.client_mail=client_mail

class Reservation:

    def __init__(self, reservation_id:int,room_id:int,client_id:int,start_date:date, end_date:date):
        self.reservation_id=reservation_id
        self.room_id=room_id
        self.client_id=client_id
        self.start_date=start_date
        self.end_date=end_date


class Chambre:

    def __init__(self, room_id:int, max_people:int, price:int, room_size:int):
        self.room_id=room_id
        self.max_people=max_people
        self.price=price
        self.room_size=room_size


class Option:

    def __init__(self, reservation_id:int, option_id:OptionPossibles) 
        self.reservation_id=reservation_id
        self.option_id=option_id

