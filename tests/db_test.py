import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from src.hotel_manager.modele.gestion_db import init_db, Base, ChambreDB, ReservationDB, ClientDB


"""Creation de la connection"""
db_test = sa.create_engine("sqlite:///test.db")

#expire_on_commit permet de récupéré des infos même après le commit avant que la session se ferme
session_test = sessionmaker(bind=db_test, expire_on_commit=False)

if __name__ == "__main__":
    Base.metadata.create_all(db_test)
    init_db(session_test)
    with session_test() as session:
        print(session.query(ChambreDB).all())
        print(session.query(ClientDB).all())
        print(session.query(ReservationDB).all())
