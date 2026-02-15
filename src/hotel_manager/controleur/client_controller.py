from src.hotel_manager.modele.gestion_db import session_db,ClientDB,add_to_db
from src.hotel_manager.controleur.controle_saisie import controler_mail, controler_telephone
import logging
from src.hotel_manager.modele.classe_objet import Client, supprimer_client_db, tous_les_clients


def creer_client(firstname_client:str,lastname_client:str,tel_client:str,mail_client:str, Session = session_db) -> Client:
    """Fonction qui permet de créer une instance chambre tout en l'enregistrant dans la base de donnée"""
    try:
        controler_telephone(tel_client)
        controler_mail(mail_client)
        lastname_client = lastname_client.upper()
        client=ClientDB(client_firstname=firstname_client,client_lastname=lastname_client,client_tel=tel_client,client_mail=mail_client)
        client=add_to_db(client, Session)
        logging.info(f"Client cree, id:{client.client_id}")
        return Client(client.client_id, client.client_firstname, client.client_lastname, client.client_tel, client.client_mail)
    except Exception as e :
        raise e

def suppression_client(id_client, Session = session_db) -> None:
    """Fonction permettant de supprimer un client à partir de son id"""
    supprimer_client_db(id_client, Session)

def afficher_tous_les_clients(Session = session_db) -> list[Client]:
    """Fonction permettant d'afficher tous les clients"""
    return tous_les_clients(Session)
