def convert_boolean_to_yes_no(boolean: bool) -> str:
    """
    Convert a boolean to a Yes/No using the following rule:
        - if `True` returns "Yes"
        - otherwise returns "No"
    """
    return "Yes" if boolean else "No"
