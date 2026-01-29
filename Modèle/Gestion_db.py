import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy import Date 
from sqlalchemy import ForeignKey
from datetime import date


db = sa.create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=db)
Base = declarative_base()


class Chambre(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key = True)
    nblit: Mapped[int]
    prix: Mapped[float]
    superficie: Mapped[int]

    def __repr__(self) -> str:
        return f"<Chambre(id={self.id}, nblit={self.nblit}, prix={self.prix}, superficie={self.superficie})>"
    


class Reservation(Base):
    __tablename__="reservation"
    reservation_id:Mapped[int]=mapped_column(primary_key=True)
    room_id:Mapped[int]=mapped_column(ForeignKey("chambre.id"))
    start_date:Mapped[date]=mapped_column(Date, nullable=False)
    end_date:Mapped[date]=mapped_column(Date, nullable=False)

    def __repr__(self) -> str:
        return f"<Reservation(id={self.reservation_id}, id_chambre={self.room_id}, date_debut={self.start_date}, date_fin={self.end_date})>"

def main() -> None:

    Base.metadata.create_all(db)
    chambre = Chambre(nblit = 2, prix =60.99, superficie = 30)
    reservation = Reservation(room_id=1,start_date=date(2026,1,8),end_date=date(2026,2,5))

    with Session() as session:
        session.add(chambre)
        session.add(reservation)
        session.commit()
        print(session.query(Chambre).all())

if __name__ == "__main__":
    main()




