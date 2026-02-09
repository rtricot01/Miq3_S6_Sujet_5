import logging

def setup_logging():
    logging.basicConfig(
        filename='Application.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
