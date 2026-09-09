def validate_required_fields(record, required_fields):
    return all(field in record for field in required_fields)