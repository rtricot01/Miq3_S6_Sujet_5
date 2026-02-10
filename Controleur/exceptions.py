class ReservationDateException(Exception):
    """Exception qui se lève en cas de mauvais choix de date"""
#TODO mettre une logger WARNING
    pass

class ObjectNotFoundException(Exception):
    """Exception qui se lève si l'objet demandé n'existe pas"""
#TODO mettre une logger WARNING
    pass