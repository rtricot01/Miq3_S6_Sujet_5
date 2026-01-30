from datetime import date

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


