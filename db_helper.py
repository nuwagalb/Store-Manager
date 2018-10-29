import psycopg2
from db_config import db_name, db_user, db_password, db_host
import psycopg2.ra

class DBHelper:
    """
        class with methods to find, add, delete and update records to the database 
    """
    table_name = 'users'
    table_fields = ['user_id', 'username', 'email', 'password', 
                    'role', 'date_created', 'date_modified']

    def create_record(self):
        record = {}
        for i in range(0, len(DBHelper.table_fields)):
            record[DBHelper.table_fields[i]] = 0
        return record

    def find_all_records(self):
        """"""
        connection = DBHelper.open_connection()
        try:
            list_of_records = []

            query = "SELECT * FROM {};".format(DBHelper.table_name)
            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
                new_record = self.create_record()
                for result in results:
                    for i in range(0, len(DBHelper.table_fields)):
                        new_record[DBHelper.table_fields[i]] = result[i]
                    list_of_records.append(new_record)
                    '''new_record['username'] = result[1]
                    new_record['email'] = result[2]
                    new_record['password'] = result[3]
                    new_record['role'] = result[4]
                    new_record['date_created'] = result[5]
                    new_record['date_modified'] = result[6]
                    list_of_records.append(new_record)'''
                
                '''if results:
                    new_record = self.create_record()
                    for result in results
                        new_record[DBHelper.table_fields[i]] = result[i]
                        list_of_records.append(new_record)'''

                return results
        finally:
           DBHelper.close_connection(connection)

    def add_input(self, data):
        connection = db.open_connection()
        try:
            query = "INSERT INTO {} (description) VALUES('{}');".format(table_name, data)
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            db.close_connection(connection)

    def clear_all(self):
        connection = db.open_connection()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            db.close_connection(connection)

    @staticmethod
    def open_connection():
        """opens up a connection to the database"""
        return psycopg2.connect(host=db_host,
                            user=db_user,
                            password=db_password,
                            dbname=db_name
                        )

    @staticmethod
    def close_connection(connection):
        """closes a connection to the database"""
        return connection.close()


test_helper = DBHelper()
records = test_helper.create_record()
details = test_helper.find_all_records()
print(records)
print(details)