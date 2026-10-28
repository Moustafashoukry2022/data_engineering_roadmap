import logging
from log_config import setup_logging_config
import file_handler as fh
import validation as va
from exceptions import DataValidationError
# 1. Configure logging
setup_logging_config()

# 2. Create logger for main.py
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Pipleline started")
    failed_to_handle=[]
    try:
        #fetch files
        files=fh.find_input_files()
        schema_file=fh.find_schema_files()
        schema=fh.read_schema(schema_file)
        #loop over files
        for file in files:
            try:
                #read data
                data=fh.read_input_data(file)
                
                validation_result=va.validate_column_schema(data,schema)
                if validation_result=="warning":
                    logger.warning("issues in the input data but pipleline can still contniue")
                else:
                    logger.info("input columns checked and are successful")
            except DataValidationError as e:
                 failed_to_handle.append(file)
                 logger.error(e)
        if failed_to_handle:
            logger.error(f"files :{failed_to_handle} failed to be handeld")
    except FileNotFoundError:
        logger.info("No csv files found")


