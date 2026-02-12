import logging

class ReservationDateException(Exception):
    """Exception qui se lève en cas de mauvais choix de date"""
    def __init__(self, message ="La date choisie n'est pas valable"):
        logging.warning(message)
        super().__init__(message)

class ObjectNotFoundException(Exception):
    """Exception qui se lève si l'objet demandé n'existe pas"""
    def __init__(self, message ="L'objet demande n'existe pas dans la base de donnee"):
        logging.warning(message)
        super().__init__(message)
    
class TelephoneNumberException(Exception):
    """Exception qui se lève si le numéro de téléphone d'un client n'est pas valable"""
    def __init__(self, message ="Le numero de telephone renseigne n'est pas valide"):
        logging.warning(message)
        super().__init__(message)

class EmailException(Exception):
    """Exception qui se lève si le numéro de téléphone d'un client n'est pas valable"""
    def __init__(self, message ="L'adresse email renseignee n'est pas valide"):
        logging.warning(message)
        super().__init__(message)