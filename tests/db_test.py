import sqlalchemy as sa
import pytest
from sqlalchemy.orm import sessionmaker
from src.hotel_manager.modele.gestion_db import init_db, Base, ChambreDB, ReservationDB, ClientDB

@pytest.fixture
def sessiontest():
    """Creation de la connexion à la DB qui supprime toute les tables 
    et les recréer à chaque fois."""
    db_test = sa.create_engine("sqlite:///test.db")
    Base.metadata.drop_all(db_test)
    Base.metadata.create_all(db_test)
    return sessionmaker(bind=db_test, expire_on_commit=False)

