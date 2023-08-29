import re

def validate_password(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{10,}$"

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)

def only_letters(string):
    """Check if the string contains only letters."""

    pattern = r"^[a-zA-Z]+$"
    match = re.match(pattern, string)

    return bool(match)

