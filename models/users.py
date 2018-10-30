from db_helper import DBHelper

class User:
    def __init__(self, email, password, role=False):
        self.email = email
        self.password = password
        self.role = role

    def get_email(self, email):
        """returns email statuus"""
        if email:
             db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
             email_status = db.find_record_by_email(email)

        if not email_status:
            return False
        return True

    def get_password(self, password):
        """returns the password status"""
        hashed_password = None
        if password:
            db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
            result = db.find_record_by_password(password)
            
        if not result:
            return "Password not found"

        hashed_password = result[2]
        return hashed_password


