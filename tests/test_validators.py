import unittest
from models.validators import Validator

class ValidatorTestCase(unittest.TestCase):
    """class with test methods for the Validator class"""
    def setUp(self):
        self.validator = Validator()

    #tests for the validate_email
    def test_validate_email_raises_a_type_error_if_no_value_is_passed(self):
        """test for type error exception"""
        with self.assertRaises(
                TypeError,
                msg="No value was passed to the validate_email method. Please enter a value"):
            self.validator.validate_email(None)

    def test_validate_email_returns__error_message_if_a_str_is_not_passed(self):
        """test for wrong data type"""
        self.assertEqual(self.validator.validate_email(45),
            "Invalid data type for the email"
        )
        self.assertEqual(self.validator.validate_email({}),
             "Invalid data type for the email"
        )
        self.assertEqual(self.validator.validate_email([]),
             "Invalid data type for the email"
        )
        self.assertEqual(self.validator.validate_email(True),
             "Invalid data type for the email"
        )

    def test_validate_email_method_returns_an_error_message_on_empty_details(self):
        """test for empty inputs in email field"""
        self.assertEqual(
            self.validator.validate_email(''),
            "Email cannot be empty. Please enter a valid email"
        )

    def test_validate_email_method_returns_an_error_message_on_invalid_email_format(self):
        """test for missing @ symbol in email address"""
        self.assertEqual(
            self.validator.validate_email('isnuwagmail.com'),
            "Invalid email address. Please enter valid address"
        )
 
    def test_validate_method_returns_true_for_a_valid_email_address(self):
        """test for valid username details"""
        self.assertEqual(
            self.validator.validate_email('isnuwa@gmail.com'),
            True
        )

    #tests for the validate_password
    def test_validate_password_raises_a_type_error_if_no_value_is_passed(self):
        """test for type error exception"""
        with self.assertRaises(
                TypeError,
                msg="No value was passed to the validate_password method. Please enter a value"):
            self.validator.validate_password(None)

    def test_validate_password_does_not_accept_empty_details(self):
        """test for empty inputs in password field"""
        self.assertEqual(
            self.validator.validate_password(''),
            "Empty password details cannot be validated."
        )

    def test_validate_password_returns_an_error_message_for_invalid_password_length(self):
        """test for short password length"""
        self.assertEqual(
            self.validator.validate_password('nuwagal'),
            "Password must be more than 7 characters"
        )
    
    def test_validate_password_returns_an_error_message_for_no_capital_letter_in_password(self):
        """test that password must contain a capital letter"""
        self.assertEqual(
            self.validator.validate_password('nuwagalb'),
            "Password must contain a capital letter"
        )

    def test_validate_password_returns_an_error_message_for_no_small_letter_in_password(self):
        """test that password must contain a small letter"""
        self.assertEqual(
            self.validator.validate_password('NUWAGALB'),
            "Password must contain a small letter"
        )

    def test_validate_password_returns_an_error_message_for_no_digit_in_password(self):
        """test that password must contain a digit"""
        self.assertEqual(
            self.validator.validate_password('NuWAGALB'),
            "Password must contain a digit"
        )

    def test_validate_password_returns_an_error_message_for_no_special_character_in_password(self):
        """test that password must contain a special character"""
        self.assertEqual(
            self.validator.validate_password('NuWAGALB2'),
            "Password must contain a special character"
        )
    
    def test_validate_password_method_returns_true_for_a_valid_password(self):
        """test for valid password details"""
        self.assertEqual(
            self.validator.validate_password('NuWAGALB2$'),
            True
        )