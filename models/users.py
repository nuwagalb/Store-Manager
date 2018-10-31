from db_helper import DBHelper

class User:
    """
        class with all the methods and attributes 
        of working with a user
    """
    def __init__(self, email, password, role=False):
        self.email = email
        self.password = password
        self.role = role

    def register(self):
        """registers a user"""
        db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        result = db.find_record(self.email)
        
        if not result:
            return db.insert_record([self.email, self.password, self.role])
        return "There already exists a user with that email address"