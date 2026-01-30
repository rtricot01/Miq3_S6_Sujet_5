import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from Gestion_db import Chambre,Base,Client, Reservation, Option, add_to_db
from datetime import date

"Etablissement de la connection avec la BDD"
db = sa.create_engine("sqlite:///hotel.db")
Session = sessionmaker(bind=db)

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


def init_db():
    Base.metadata.create_all(db)
    init_chambre()
    with Session() as session:
        print(session.query(Chambre).all())
    
if __name__ == "__main__":
    init_db()