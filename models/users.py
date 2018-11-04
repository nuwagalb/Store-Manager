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
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        User.admin_creation()

    @staticmethod
    def admin_creation():
        """creates admin details for the first user of the application"""
        db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        
        if not db.find_all_records():
            hashed_password = generate_password_hash('Admin@123')
            db.insert_record(['admin@storemanager.com', hashed_password, 'admin'])

    def get_record(self, value):
        """returns any given record"""
        if value:
            result = self.db.find_record(value)

        if not result:
            return {}
        return result

    def register(self):
        """registers a user"""
        inserted_id = 0
        result = self.db.find_record(self.email)
        
        if not result:
            inserted_row = self.db.insert_record([self.email, self.password, self.role])
            inserted_id = inserted_row.get('user_id')
        
        if inserted_id:
            return self.db.find_record_by_id(inserted_id)

        return {}
        