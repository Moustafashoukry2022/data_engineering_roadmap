import logging 
def setup_logging_config():
    logging.basicConfig(
        level=logging.DEBUG,
        filename="C:\\Mine folder\\data_engineering_roadmap\\automated_data_platform\\logs\\pipeline.log",
        filemode="a",
        format="%(asctime)s | %(levelname)s | %(message)s"
    )

