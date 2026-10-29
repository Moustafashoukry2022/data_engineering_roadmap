#config logging
import logging
logger = logging.getLogger(__name__)

#packages
import pandas as pd
import json
import os
from pathlib import Path

#file location
BASE_DIR=Path(__file__).resolve().parent.parent
input_folder=BASE_DIR / "input"
output_folder=BASE_DIR / "output"
schema_folder=BASE_DIR / "schema"

def find_input_files():
    logger.info("Started fetching files")
    input_files=[]
    for file in os.listdir(input_folder):
        if file.lower().endswith(".csv"):
            input_files.append(file)
    if not input_files:
        raise FileNotFoundError("No files found")
    else:
        logger.info(f"finished fetching files found: {len(input_files)} files")
        return input_files
    
def find_schema_files():
    logger.info("Started fetching schema")
    schema_file=None    
    for file in os.listdir(schema_folder):
        if file.lower().endswith(".json"):
            schema_file=file
    if not schema_file:
        raise FileNotFoundError("No schema file found")
    else:
        logger.info(f"Schema file found {schema_file}")
        return schema_file


def read_schema(filename):
    with open (schema_folder / filename,"r") as file:
        schema=json.load(file)
    return schema


def read_input_data(filename):
    logger.info(f"reading file {filename}")
    data=pd.read_csv(input_folder / filename)
    return data

def create_file(location,filename,data):
    data=pd.DataFrame(data)
    data.to_csv(BASE_DIR / location / filename , index=False)



    