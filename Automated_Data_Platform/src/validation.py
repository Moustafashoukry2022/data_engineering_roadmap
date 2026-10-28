#config logging
import logging
logger = logging.getLogger(__name__)

#packages
from exceptions import DataValidationError
from file_handler import read_schema



def validate_column_schema(data,schema):
    logger.info("checking column avaliablty and order")
    expected_columns=list(schema)
    data.columns = (data.columns.str.strip().str.lower().str.replace(" ", "_"))
    actual_data= data.columns.tolist()

    # lists
    missing_col=[]
    extra_col=[]
    duplicated_col={}
    actual_order=[]

    #loops
    for col in expected_columns:
        if col not in actual_data:
            missing_col.append(col)
    for col in actual_data:
        if col not in expected_columns:
            extra_col.append(col)
        else:
            actual_order.append(col)
        count=actual_data.count(col)
        if count>1:
            duplicated_col[col]=count
    if not missing_col and not duplicated_col and actual_order!=expected_columns:
        logger.warning("Wrong column order")
    if extra_col:
         logger.warning(f"Extra columns: {extra_col}")
    if duplicated_col:
        logger.error(f"Duplicated columns: {duplicated_col}")

    if missing_col:
        logger.error(f"Missing columns: {missing_col}")

    if missing_col or duplicated_col:
        raise DataValidationError("Column validation failed")
    return "success" if actual_data == expected_columns else "warning"

