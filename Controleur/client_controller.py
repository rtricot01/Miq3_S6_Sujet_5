from datetime import date
from Modele.gestion_db import session_db,ClientDB,add_to_db
from Modele.exceptions import ReservationDateException, TelephoneNumberException, EmailException
from Controleur.controle_saisie import controler_mail, controler_telephone
import logging
from Modele.classe_objet import Client, supprimer_client_db, tous_les_clients
from tests.db_test import session_test


def creer_client(firstname_client:str,lastname_client:str,tel_client:str,mail_client:str, Session = session_db) -> Client:
    """Fonction qui permet de créer une instance chambre tout en l'enregistrant dans la base de donnée"""
    try:
        controler_telephone(tel_client)
        controler_mail(mail_client)
        lastname_client = lastname_client.upper()
        client=ClientDB(client_firstname=firstname_client,client_lastname=lastname_client,client_tel=tel_client,client_mail=mail_client)
        client=add_to_db(client, Session)
        logging.info(f"Client créée, id:{client.client_id}")
        return Client(client.client_id, client.client_firstname, client.client_lastname, client.client_tel, client.client_mail)
    #TODO Exception à changer
    except Exception as e :
        raise e

def suppression_client(id_client, Session = session_db):
    """Fonction permettant de supprimer un client à partir de son id"""
    supprimer_client_db(id_client, Session)

def afficher_tous_les_clients(Session = session_db):
    """Fonction permettant d'afficher tous les clients"""
    return tous_les_clients(Session)

print(tous_les_clients(session_test))