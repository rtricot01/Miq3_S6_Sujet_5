import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

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

"""Creation des chambres présentes au lancement de l'application"""
def init_chambre() -> None:

    chambre1 = Chambre(max_people = 2, prize= 60.99, room_size = 30)
    add_to_db(chambre1)


"""Fonction Main"""
def main() -> None:
    Base.metadata.create_all(db)
    init_chambre()
    with Session() as session:
        print(session.query(Chambre).all())

if __name__ == "__main__":
    main()
