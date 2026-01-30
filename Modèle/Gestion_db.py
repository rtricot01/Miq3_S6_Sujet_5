import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy import Date 
from sqlalchemy import ForeignKey
from datetime import date
from Creation_db import Session

Base = declarative_base()

"""Ajout de n'importe quel objet à la BDD"""
def add_to_db(object)-> None:
    with Session() as session:
        session.add(object)
        session.commit()


"""Table chambre et classe Python"""
class Chambre(Base):
    __tablename__ = "chambre"
    room_id: Mapped[int] = mapped_column(primary_key = True)
    max_people: Mapped[int]
    prize: Mapped[float]
    room_size: Mapped[int]

    def __repr__(self) -> str: 
      return f"<Chambre(id={self.room_id}, nblit={self.max_people}, prix={self.prize}, superficie={self.room_size})>"
     
"""Table reservation et classe Python"""
class Reservation(Base):
    __tablename__="reservation"
    reservation_id:Mapped[int]=mapped_column(primary_key=True)
    room_id:Mapped[int]=mapped_column(ForeignKey("chambre.room_id"))
    client_id:Mapped[int]=mapped_column(ForeignKey("client.client_id"))
    start_date:Mapped[date]=mapped_column(Date, nullable=False)
    end_date:Mapped[date]=mapped_column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<Reservation(id={self.reservation_id}, id_chambre={self.room_id}, date_debut={self.start_date}, date_fin={self.end_date})>"
       
"""Table Client et classe python"""
class Client(Base):
    __tablename__="client"
    client_id:Mapped[int]=mapped_column(primary_key=True)
    client_firstname:Mapped[str]
    client_lastname:Mapped[str]
    client_tel:Mapped[str]
    client_mail:Mapped[str]
    
    def __repr__(self) -> str:
        return f"<Client(client_id={self.client_id}, client_firstname={self.client_firstname}, client_lastname={self.client_lastname}, client_tel={self.client_tel}, client_mail={self.client_mail})>"

"""Table Client et classe python"""
class Option(Base):
    """Une table contenant deux colonnes, une première avec l'id de la reservation et un seconde avec l'id des options.
    On peut avoir plusieurs lignes avec le même id de reservation mais avec de id d'option différent"""
    __tablename__="option"
    reservation_id:Mapped[int]=mapped_column(ForeignKey("reservation.reservation_id"))
    option_id:Mapped[int]  

    def __repr__(self)->str:
        return f"Option(reservation_id={self.reservation_id}, option_id={self.option_id})"
    





