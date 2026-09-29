import json 
import os 
import logging 


#log configuration

logger = logging.getLogger(__name__)


#global variables
input_directory="C:\\Mine folder\\data_engineering_roadmap\\automated_data_platform\\data\\input"
output_directory="C:\\Mine folder\\data_engineering_roadmap\\automated_data_platform\\data\\output"




#search for all input json files
def find_input_file():
    input_files=[]
    try:
        logger.info("started searching for json input files")
        for file in os.listdir(input_directory):
            if file.endswith("json"):
                input_files.append(file)
        if not input_files:
            raise FileNotFoundError()
        return input_files
    except FileNotFoundError as e:
        logger.error("No json file/s found")
        raise FileNotFoundError
        
#reading input data from files
def read_input_file (filename):
    logger.info(f"reading file:{filename}")
    with open (f"{input_directory}\\{filename}","r") as file:
        input_data=json.load(file)
    return input_data

#writing data to output files
def write_data(output_filename,data,mode):
    logger.info(f"writing to file:{output_filename}")
    with open(f"{output_directory}\\{output_filename}",mode) as file:
        json.dump(data,file,indent=4)
    





