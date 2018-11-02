from db_helper import DBHelper
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """
        class with all the methods and attributes 
        of working with a user
    """
    def __init__(self, email, password, role="attendant"):
        self.email = email
        self.password = password
        self.role = role
        User.admin_creation()

    @staticmethod
    def admin_creation():
        """creates a new admin at setting up of the database"""
        db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        
        if not db.find_all_records():
            hashed_password = generate_password_hash('Admin@123')
            db.insert_record(['admin@storemanager.com', hashed_password, 'admin'])

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
            db.insert_record([self.email, self.password, self.role])
            inserted_user = db.find_record(self.email)
            return inserted_user
        return "There already exists a user with that email address"
