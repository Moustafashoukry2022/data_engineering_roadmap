#config logging
import logging
logger = logging.getLogger(__name__)

#packages
from exceptions import DataValidationError
from file_handler import read_schema
import pandas as pd


def validate_column_schema(data,schema):
    logger.info("checking column avaliablty and order")
    expected_columns=list(schema["schema"])
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



def validation_report(col,invalid,expected_data_type):
    validation_data=[]
    for index,value in col.loc[invalid].items():
        validation_data.append({
            "column_name":col.name,
            "row_number":index+2,
            "value":value,
            "expected_data_type" : expected_data_type,
            "current_data_type" : str(col.dtype)
        })
    logger.debug(validation_data)
    return validation_data


def try_convertion(col,value):

    if value in('float','integer'):
        converted = pd.to_numeric(col, errors="coerce")
        invalid = converted.isna() & col.notna()
        if invalid.any():
            return validation_report(col,invalid,value),False
        if value=='float':
            col=converted.astype(float)
            return col,True
        if value=='integer':
            float_value= col.notna()  & (converted % 1 !=0)
            if float_value.any():
                return validation_report(col,float_value,value),False
            else:
                col=converted.astype("Int64")
                return col,True
            
    if value =='string':
        col = col.astype('string')
        return col,True
    
    if value == 'datetime':
        converted = pd.to_datetime(col, errors="coerce")
        invalid = converted.isna() & col.notna()
        if invalid.any():
            return validation_report(col,invalid,value),False
        else:
            col=converted.astype("datetime64[ns]")
            return col,True
        
    if value == "boolean":
        valid_values = [
        True, False,
        "True", "False",
        1, 0, 1.0, 0.0,
        "1", "0", "1.0", "0.0"
        ]
        invalid = ~col.isin(valid_values) & col.notna()
        if invalid.any():
            return validation_report(col, invalid,value),False
        converted = col.astype("string").str.lower().map({
            "true": True,
            "false": False,
            "1": True,
            "0": False,
            "1.0": True,
            "0.0": False
        })

        return converted.astype("boolean"),True


def data_type_validation(data,schema,filename):
    logger.info("started data validation")
    validation_list=[]
    expected_data_type=schema["schema"]
    column_error_count=0
    for key,value in expected_data_type.items():
        if    (
               (value =='float' and (not str(data[key].dtype).lower().startswith('int') and not str(data[key].dtype).startswith('float')))
            or (value =='integer' and (not str(data[key].dtype).lower().startswith('int')))
            or (value =='string' and (not str(data[key].dtype).startswith('str')))
            or (value =='datetime' and (not str(data[key].dtype).startswith('date')))
            or (value =='boolean' and (not str(data[key].dtype).startswith('bool')))
              ):
            converted,status=try_convertion(data[key],value)
            if status:
                data[key]=converted
            else:
                validation_list.extend(converted)
                column_error_count+=1
    logger.debug(f" data type validation {validation_list}")
    return column_error_count,data,validation_list
        
            

    


