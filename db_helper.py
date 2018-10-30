import psycopg2
from db_config import prod_db_name, db_user, db_password, db_host, test_db_name
from v2.api.views import  api

class DBHelper:
    """
        class with methods to find, add, delete and
        update records to the database
    """
    def __init__(self, table_name, table_fields):
        self.table_name = table_name
        self.table_fields = table_fields
        self.conn = DBHelper.open_connection()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    # def insert_record(self):
    #     # for i in range(0, len(self.table_fields)):
    #     #     if class_name == 
    #     # return record
    #     pass

    def find_record_by_id(self, record_id):
        """finds a record by it's id"""       
        sql = """SELECT * 
                 FROM {} 
                 WHERE {} = {}
              """.format(self.table_name, self.table_fields[0], record_id)
        self.cur.execute(sql)
        result = self.cur.fetchone()

        return result

    def find_all_records(self):
        """finds all records"""
        sql = "SELECT * FROM {}".format(self.table_name)
        self.cur.execute(sql)
        results = self.cur.fetchall()

        return results
        
    def update_a_record(self, field_name, name_value, field_id, id_value):
        """updates a records's name"""
        sql = """ UPDATE {}
                SET {} = {}
                WHERE {} ={}
            """.format(self.table_name, field_name, name_value, field_id, id_value)
        self.cur.execute(sql)
        updated_rows = self.cur.rowcount

        return updated_rows

    def delete_record(self, record_id):
        """deletes a record from the database"""
        sql = """DELETE
                 FROM {} 
                 WHERE {} = {}
              """.format(self.table_name, self.table_fields[0], record_id)
        self.cur.execute(sql)

        return True

    @staticmethod
    def open_connection():
        """opens up a connection to the database"""
        try:
            if api.config['TEST_DB'] == 'testing':
                db_name = test_db_name
            else:
                db_name = prod_db_name

            connection = psycopg2.connect(host=db_host,
                            user=db_user,
                            password=db_password,
                            dbname=db_name
                        )
            return connection
        except psycopg2.Error as error:
            print(error)

    @staticmethod
    def close_connection(connection):
        """closes a connection to the database"""
        return connection.close()
