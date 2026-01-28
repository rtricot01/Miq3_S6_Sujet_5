import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base

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

def main() -> None:
    Base.metadata.create_all(db)
    chambre = Chambre(nblit = 2, prix =60.99, superficie = 30)

    with Session() as session:
        session.add(chambre)
        session.commit()
        print(session.query(Chambre).all())

if __name__ == "__main__":
    main()
