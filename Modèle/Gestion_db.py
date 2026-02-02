import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy import Date 
from sqlalchemy import ForeignKey
from datetime import date
from enum import IntEnum

"""Creation de la connection"""
db = sa.create_engine("sqlite:///hotel.db")

#expire_on_commit permet de récupéré des infos même après le commit avant que la session se ferme
Session = sessionmaker(bind=db, expire_on_commit=False)
Base = declarative_base()

"""Creation de la BDD"""
def init_db():
    init_chambre()
    init_client()
    init_reservation()
    init_option()

"""Ajout de n'importe quel objet à la BDD"""
def add_to_db(object):
    with Session() as session:
        session.add(object)
        session.commit()
#on retourne l'objet qui continent l'id de l'objet créé
    return object
         

"""Table chambre"""
class ChambreDB(Base):
    __tablename__ = "chambre"
    room_id: Mapped[int] = mapped_column(primary_key = True)
    max_people: Mapped[int]
    prize: Mapped[float]
    room_size: Mapped[int]

    def __repr__(self) -> str: 
      return f"<Chambre(id={self.room_id}, nblit={self.max_people}, prix={self.prize}, superficie={self.room_size})>"

"""Creation des chambres présents au lancement de l'application"""
def init_chambre() -> None:

    for i in range(4):
        chambre = ChambreDB(max_people = 2, prize= 60.99, room_size = 30)
        add_to_db(chambre)
        chambre = ChambreDB(max_people = 3, prize = 70.99, room_size = 35)
        add_to_db(chambre)
        chambre = ChambreDB(max_people = 4, prize = 80.99, room_size = 40)
        add_to_db(chambre)   

"""Table reservation"""
class ReservationDB(Base):
    __tablename__="reservation"
    reservation_id:Mapped[int]=mapped_column(primary_key=True)
    room_id:Mapped[int]=mapped_column(ForeignKey("chambre.room_id"))
    client_id:Mapped[int]=mapped_column(ForeignKey("client.client_id"))
    start_date:Mapped[date]=mapped_column(Date, nullable=False)
    end_date:Mapped[date]=mapped_column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<Reservation(id={self.reservation_id}, id_chambre={self.room_id}, date_debut={self.start_date}, date_fin={self.end_date})>"

"""Creation des réservations présents au lancement de l'application"""
def init_reservation() -> None:

    reservation = ReservationDB(room_id=1,client_id=1,start_date=date(2026,1,8),end_date=date(2026,2,5))
    add_to_db(reservation)

"""Table Client"""
class ClientDB(Base):
    __tablename__="client"
    client_id:Mapped[int]=mapped_column(primary_key=True)
    client_firstname:Mapped[str]
    client_lastname:Mapped[str]
    client_tel:Mapped[str]
    client_mail:Mapped[str]
    
    def __repr__(self) -> str:
        return f"<Client(client_id={self.client_id}, client_firstname={self.client_firstname}, client_lastname={self.client_lastname}, client_tel={self.client_tel}, client_mail={self.client_mail})>"
    
"""Creation des clients présents au lancement de l'application"""
def init_client() -> None:

    client = ClientDB(client_firstname = "Quentin", client_lastname= "LEVEQUE",client_tel="0102030405",client_mail="bogoss@gmail.com")
    add_to_db(client)

"""Table Option"""
class OptionDB(Base):
    """Une table contenant deux colonnes, une première avec l'id de la reservation et un seconde avec l'id des options.
    On peut avoir plusieurs lignes avec le même id de reservation mais avec de id d'option différent"""
    __tablename__="option"
    option_id: Mapped[int]=mapped_column(primary_key=True)
    reservation_id:Mapped[int]=mapped_column(ForeignKey("reservation.reservation_id"))
    option_id:Mapped[int]  

    def __repr__(self)->str:
        return f"Option(reservation_id={self.reservation_id}, option_id={self.option_id})"

"""Differentes options possibles"""
class OptionsPossibles(IntEnum):
    SPA = 1
    PETIT_DEJEUNER = 2
    PARKING = 3
    WIFI = 4

"""Creation des Options présents au lancement de l'application"""
def init_option() -> None:

    option= OptionDB(reservation_id = 1,option_id = OptionsPossibles.SPA)
    add_to_db(option)
    option = OptionDB(reservation_id = 1,option_id = OptionsPossibles.PETIT_DEJEUNER)
    add_to_db(option)

if __name__ == "__main__":
    Base.metadata.create_all(db)
    init_db()
    with Session() as session:
        print(session.query(ChambreDB).all())
        print(session.query(ClientDB).all())
        print(session.query(ReservationDB).all())
        print(session.query(OptionDB).all())
