import os
from hotel_manager.modele.gestion_db import Base, db, init_db, session_db

def setup_database() -> None:
    if os.path.exists("hotel.db"):
        os.remove("hotel.db")
        print("Ancienne base supprimée.")

    print("Création de la nouvelle base de données")
    Base.metadata.create_all(db)
    init_db(session_db)
    print("Base de données hotel.db créée ")

if __name__ == "__main__":
    setup_database()