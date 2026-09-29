import logging




logger = logging.getLogger(__name__)

def  validate_data(data):
    logger.info("validation started")
    total_rows_count=0
    bad_rows_count=0
    good_rows=[]
    bad_rows=[]

    for row in data["customers"]:
        errors=[]
        if not row.get("country"):
            row["country"]="Unknown"
        if type(row.get("id"))==int and row["name"]!= "" and type(row.get("name"))==str:
            good_rows.append(row)
        else:
            if type(row.get("id"))!=int:
                errors.append("id must be an integer")
            if type(row.get("name"))==str:
                errors.append(f"wrong name type:{type(row.get("name"))}")
            if row["name"]!= "":
                errors.append("name must not be empty")
            row["errors"]=errors
            logger.debug(row)
            bad_rows.append(row)
            bad_rows_count+=1
        total_rows_count+=1
    logger.info(
        f"""validation finished
            total rows found:{total_rows_count} 
            "bad rows found:{bad_rows_count}
            "valid rows found:{total_rows_count-bad_rows_count}""")
    return bad_rows,good_rows
    