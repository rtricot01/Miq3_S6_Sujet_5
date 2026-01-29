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
     
    
class Reservation(Base):
    __tablename__="reservation"
    reservation_id:Mapped[int]=mapped_column(primary_key=True)
    room_id:Mapped[int]=mapped_column(ForeignKey("chambre.id"))
    start_date:Mapped[date]=mapped_column(Date, nullable=False)
    end_date:Mapped[date]=mapped_column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<Reservation(id={self.reservation_id}, id_chambre={self.room_id}, date_debut={self.start_date}, date_fin={self.end_date})>"
       

"""Creation des chambres présentes au lancement de l'application"""
def init_chambre() -> None:

    chambre1 = Chambre(max_people = 2, prize= 60.99, room_size = 30)
    add_to_db(chambre1)


"""Fonction Main"""
def main() -> None:

    Base.metadata.create_all(db)
    
    reservation = Reservation(room_id=1,start_date=date(2026,1,8),end_date=date(2026,2,5))

  
    init_chambre()
    with Session() as session:
        print(session.query(Chambre).all())

if __name__ == "__main__":
    main()




