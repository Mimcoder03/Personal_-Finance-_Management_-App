import getpass

def get_numeric_input(prompt, type_func=float, error_msg="Invalid input. Please enter a valid number."):
    """
    Repeatedly prompts the user for numeric input until a valid value is provided.
    """
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                return None  # Allows for optional inputs if handled by caller
            return type_func(val)
        except ValueError:
            print(error_msg)

def get_non_empty_input(prompt, error_msg="Input cannot be empty. Please try again.", is_password=False):
    """
    Repeatedly prompts the user until a non-empty string is provided.
    """
    while True:
        if is_password:
            val = getpass.getpass(prompt).strip()
        else:
            val = input(prompt).strip()
        
        if val:
            return val
        print(error_msg)

def get_date_input(prompt, format="%d-%m-%Y", error_msg="Invalid date format. Please use DD-MM-YYYY."):
    """
    Validates date input against a specific format.
    """
    from datetime import datetime
    while True:
        val = input(prompt).strip()
        if not val:
            return None
        try:
            datetime.strptime(val, format)
            return val
        except ValueError:
            print(error_msg)
