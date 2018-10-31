from db_helper import DBHelper

class User:
    """
        class with all the methods and attributes 
        of working with a user
    """
    def __init__(self, email, password, role="admin"):
        self.email = email
        self.password = password
        self.role = role

    def get_email(self, email):
        """returns email statuus"""
        if email:
             db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
             result = db.find_record_by_email(email)

        if not result:
            return False
        return result[1]

    def get_password(self, email):
        """returns the password status"""
        if email:
            db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
            result = db.find_password(email)
            
        if not result:
            return "Password could not be found"

        return result[0]
    def register(self):
        """registers a user"""
        db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        result = db.find_record(self.email)
        
        if not result:
            return db.insert_record([self.email, self.password, self.role])
        return "There already exists a user with that email address"
