class DataValidationError(Exception):
    """Base exception for data validation errors."""
    pass



class WrongColumnOrder(DataValidationError):
    """Raised Columns are in wrong order."""
    pass