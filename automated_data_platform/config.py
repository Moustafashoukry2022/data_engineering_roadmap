import logging 
def setup_logging_config():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="pipleline.log",
        filemode="a",
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

