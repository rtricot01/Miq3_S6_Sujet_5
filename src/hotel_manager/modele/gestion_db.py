import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy import Date 
from sqlalchemy import ForeignKey
from datetime import date
import logging


"""Creation de la connection"""
db = sa.create_engine("sqlite:///hotel.db")

#expire_on_commit permet de récupérer des infos même après le commit avant que la session se ferme
session_db = sessionmaker(bind=db, expire_on_commit=False)
Base = declarative_base()

def init_db(Session = session_db) -> None:
    """Creation de la BDD"""
    init_chambre(Session)
    init_client(Session)
    init_reservation(Session)

def add_to_db(object, Session = session_db) -> object:
    """Ajout de n'importe quel objet à la BDD"""
    with Session() as session:
        session.add(object)
        session.commit()
    logging.info(f"Ajout de {object} dans la bdd")
#on retourne l'objet qui continent l'id de l'objet créé
    return object
         
class ChambreDB(Base):
    """Table chambre"""
    __tablename__ = "chambre"
    room_id: Mapped[int] = mapped_column(primary_key = True)
    max_people: Mapped[int]
    prize: Mapped[float]
    room_size: Mapped[int]
    animaux_toleres: Mapped[bool]
    fumeur: Mapped[bool]
    climatisation: Mapped[bool]

    def __repr__(self) -> str: 
      return f"<Chambre(id={self.room_id}, nblit={self.max_people}, prix={self.prize}, superficie={self.room_size}, animaux_toleres={self.animaux_toleres}, fumeur={self.fumeur}, climatisation={self.climatisation})>"

def init_chambre(Session = session_db) -> None:
    """Creation des chambres présents au lancement de l'application"""
    for i in range(4):
        chambre = ChambreDB(max_people = 2, prize= 60.99, room_size = 30, animaux_toleres = False, fumeur = True, climatisation = True)
        add_to_db(chambre, Session)
        chambre = ChambreDB(max_people = 3, prize = 70.99, room_size = 35, animaux_toleres = True, fumeur = False, climatisation = False)
        add_to_db(chambre, Session)
        chambre = ChambreDB(max_people = 4, prize = 80.99, room_size = 40, animaux_toleres = True, fumeur = True, climatisation = False)
        add_to_db(chambre, Session)   

class ReservationDB(Base):
    """Table reservation"""
    __tablename__="reservation"
    reservation_id:Mapped[int]=mapped_column(primary_key=True)
    room_id:Mapped[int]=mapped_column(ForeignKey("chambre.room_id"))
    client_id:Mapped[int]=mapped_column(ForeignKey("client.client_id"))
    nombre_personnes : Mapped[int]
    start_date:Mapped[date]=mapped_column(Date, nullable=False)
    end_date:Mapped[date]=mapped_column(Date, nullable=False)
    spa : Mapped[bool]
    petit_dejeuner : Mapped[bool]
    parking: Mapped[bool]
    wifi: Mapped[bool]

    def __repr__(self) -> str:
        return f"<Reservation(id={self.reservation_id}, id_chambre={self.room_id}, id_client={self.client_id}, nombre de personnes={self.nombre_personnes}, date_debut={self.start_date}, date_fin={self.end_date}, spa={self.spa}, petit déjeuner={self.petit_dejeuner}, parking={self.parking},wifi={self.wifi})>"

def init_reservation(Session = session_db) -> None:
    """Creation des réservations présents au lancement de l'application"""
    reservation = ReservationDB(room_id=1,client_id=1,nombre_personnes=2,start_date=date(2026,1,8),end_date=date(2026,2,5), spa=True, petit_dejeuner =True, parking = True, wifi = False)
    add_to_db(reservation, Session)

class ClientDB(Base):
    """Table Client"""
    __tablename__="client"
    client_id:Mapped[int]=mapped_column(primary_key=True)
    client_firstname:Mapped[str]
    client_lastname:Mapped[str]
    client_tel:Mapped[str]
    client_mail:Mapped[str]
    
    def __repr__(self) -> str:
        return f"<Client(client_id={self.client_id}, client_firstname={self.client_firstname}, client_lastname={self.client_lastname}, client_tel={self.client_tel}, client_mail={self.client_mail})>"
    
def init_client(Session = session_db) -> None:
    """Creation des clients présents au lancement de l'application"""
    client = ClientDB(client_firstname = "Quentin", client_lastname= "LEVEQUE",client_tel="0102030405",client_mail="bogoss@gmail.com")
    add_to_db(client, Session)