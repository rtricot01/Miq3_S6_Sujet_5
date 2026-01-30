import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy import Date 
from sqlalchemy import ForeignKey
from datetime import date


db = sa.create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=db)
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

"""Creation des chambres présentes au lancement de l'application"""
def init_client() -> None:

    client_1 = Client(client_firstname = "ahmet", client_lastname= "tunc",client_tel="0102030405",client_mail="bogoss@gmail.com")
    add_to_db(client_1)

def init_chambre() -> None:

    chambre_1 = Chambre(max_people = 2, prize= 60.99, room_size = 30)
    add_to_db(chambre_1)

def init_reservation() -> None:

    reservation_1 = Reservation(room_id=1,client_id=1,start_date=date(2026,1,8),end_date=date(2026,2,5))
    add_to_db(reservation_1)
"""Fonction Main"""
def main() -> None:

    Base.metadata.create_all(db)
    
   
    init_chambre()
    init_client()
    init_reservation()
    
    with Session() as session:
        print(session.query(Chambre).all())
        print(session.query(Client).all())
        print(session.query(Reservation).all())

if __name__ == "__main__":
    main()




