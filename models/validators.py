import re

class Validator:
    """Class that handles the validation of the username, password,
       email, product id, and sales id
    """
    @staticmethod
    def validate_email(email):
        """validates email details"""
        messages = []

        if isinstance(email, type(None)):
            raise TypeError("No value was passed to the " \
                            "validate_email method. Please enter a value")

        if not isinstance(email, str):
            return "Invalid data type for the email"

        if not email:
            return "Email cannot be empty. Please enter a valid email"

        if not re.search(r'([\w]+)@([a-z]+)\.([a-z])', email):
            return "Invalid email address. Please enter valid address"

        for message in messages:
            return message

        return True

    @staticmethod
    def validate_password(password):
        """validates password details"""
        messages = []
        if isinstance(password, type(None)):
            raise TypeError("No value was passed to the " \
                            "validate_username method. Please enter a value")

        if not password:
            messages.append("Empty password details cannot be validated.")

        if len(password) < 8:
            messages.append("Password must be more than 7 characters")

        if not re.search(r'[A-Z]', password):
            messages.append("Password must contain a capital letter")

        if not re.search(r'[a-z]', password):
            messages.append("Password must contain a small letter")

        if not re.search(r'[0-9]', password):
            messages.append("Password must contain a digit")

        if not re.search(r'[^a-zA-Z0-9]', password):
            messages.append("Password must contain a special character")

        for message in messages:
            return message

        return True