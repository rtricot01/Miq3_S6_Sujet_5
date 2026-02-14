import re
from src.hotel_manager.modele.exceptions import TelephoneNumberException, EmailException

EMAIL_REGEX= r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

def controler_telephone(telephone: str) -> bool:
    if (telephone.isdigit()):
        pass
    else:
        raise TelephoneNumberException

def controler_mail(mail: str) -> bool:
    if re.match(EMAIL_REGEX, mail):
        pass
    else:
        raise EmailException