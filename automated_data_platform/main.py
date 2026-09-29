import logging
from data_handler import find_input_file,read_input_file,write_data
from validation import validate_data
logging.basicConfig(
    level=logging.DEBUG,
    filename="C:\\Mine folder\\data_engineering_roadmap\\automated_data_platform\\logs\\pipleline.log",
    filemode="a",
    format="%(asctime)s | %(filename)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

try:

    files=find_input_file()
    all_bad_rows={}
    all_good_rows={}
    for file in files:
        data=read_input_file(file)
        bad_rows,good_rows=validate_data(data)
        all_bad_rows[file]=bad_rows
        all_good_rows[file]=good_rows
        

    if all_bad_rows:
            write_data("invalid_customers.json",all_bad_rows,"w")
    if all_good_rows:
            write_data("valid_customers.json",all_good_rows,"w")
except Exception as e:
    logger.exception(f"unexcpected error,{e}")