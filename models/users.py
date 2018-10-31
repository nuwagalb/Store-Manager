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

    def initial_login(self):
        """this method registers the first user as the admin of the system"""
        db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        results = db.find_all_records()

        if not results:
            db.insert_record([self.email, self.password, self.role])
            self.register()
        self.role = "attendant"

    def get_email(self, email):
        """returns email statuus"""
        if email:
             db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
             result = db.find_record_by_email(email)

        if not result:
            return False
        return result

    def get_password(self, email):
        """returns the password status"""
        if email:
            db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
            result = db.find_password(email)
            
        if not result:
            return "Password could not be found"

        return result.get('password')

    def register(self):
        """registers a user"""
        db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        result = db.find_record(self.email)
        
        if not result:
            return db.insert_record([self.email, self.password, self.role])
        return "There already exists a user with that email address"
