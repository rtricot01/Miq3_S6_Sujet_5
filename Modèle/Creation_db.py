import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from Gestion_db import Chambre,Base

"Etablissement de la connection avec la BDD"
db = sa.create_engine("sqlite:///hotel.db")
Session = sessionmaker(bind=db)

"""Creation des chambres présentes au lancement de l'application"""
def init_chambre() -> None:
    chambre1 = Chambre(max_people = 2, prize= 60.99, room_size = 30)
    add_to_db(chambre1)

"""Ajout de n'importe quel objet à la BDD"""
def add_to_db(object)-> None:
    with Session() as session:
        session.add(object)
        session.commit()

def init_db():
    Base.metadata.create_all(db)
    init_chambre()
    with Session() as session:
        print(session.query(Chambre).all())
    
if __name__ == "__main__":
    init_db()