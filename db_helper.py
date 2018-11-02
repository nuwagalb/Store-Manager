import psycopg2
from psycopg2.extras import RealDictCursor
from db_config import prod_db_name, db_user, db_password, db_host, test_db_name
import os

class DBHelper:
    """
        class with methods to find, add, delete and
        update records to the database
    """
    def __init__(self, table_name, table_fields):
        self.table_name = table_name
        self.table_fields = table_fields
        self.all_sales = []
        self.conn = DBHelper.open_connection()
        self.conn.autocommit = True
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    def insert_record(self, record):
        """inserts a record into the database"""
        message = None

        if self.table_fields[0] == 'user_id':
            sql = """INSERT INTO 
                {}({}, {}, {})
                VALUES('{}', '{}', '{}')
                """.format(
                        self.table_name,
                        self.table_fields[1],
                        self.table_fields[2],
                        self.table_fields[3],
                        record[0],
                        record[1],
                        record[2]
                    )
            self.cur.execute(sql)
            message = "{} successfully created".format(record[0])

        if self.table_fields[0] == 'category_id':
            sql = """INSERT INTO 
                {}({})
                VALUES('{}')
                """.format(
                    self.table_name,
                    self.table_fields[1],
                    record[0])
            self.cur.execute(sql)
            message = "{} successfully created".format(record[0])	

        if self.table_fields[0] == 'product_id':
            sql = """INSERT INTO 
                {}({}, {}, {})
                VALUES('{}', '{}', '{}')
                """.format(
                        self.table_name,
                        self.table_fields[1],
                        self.table_fields[2],
                        self.table_fields[3],
                        record[0],
                        record[1],
                        record[2]
                    )
            self.cur.execute(sql)
            message = "{} successfully added".format(record[0])

        if self.table_fields[0] == 'sales_id':
            sql = """INSERT INTO 
                    {}({}, {}, {})
                    VALUES('{}', '{}', '{}')
            """.format(
                self.table_name,
                self.table_fields[1],
                self.table_fields[2],
                self.table_fields[3],
                record[0],
                record[1],
                record[2])
            self.cur.execute(sql)

        return message

    def find_record(self, value):
        """finds a record by a given value"""       
        sql = """SELECT * 
                 FROM {} 
                 WHERE {} = '{}'
              """.format(self.table_name, self.table_fields[1], value)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def find_password(self, email):
        """finds a record by password"""       
        sql = """SELECT password 
                 FROM {} 
                 WHERE {} = '{}'
              """.format(self.table_name, self.table_fields[1], email)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def find_record_by_email(self, email):
        """finds a record by email"""       
        sql = """SELECT * 
                 FROM {} 
                 WHERE {} = '{}'
              """.format(self.table_name, self.table_fields[1], email)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

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
        
    def update_record(self, field_name, name_value, field_id, id_value):
        """updates a records's name"""
        sql = """ UPDATE {}
                SET {} = '{}'
                WHERE {} ={}
            """.format(self.table_name, field_name, name_value, field_id, id_value)
        self.cur.execute(sql)
        updated_rows = self.cur.rowcount

        if not updated_rows:
            return {'message': 'Record could not be updated'}

        updated_record = self.find_record_by_id(id_value)

        return updated_record

    def delete_record(self, record_id):
        """deletes a record from the database"""
        sql = """DELETE
                 FROM {} 
                 WHERE {} = {}
              """.format(self.table_name, self.table_fields[0], record_id)
        self.cur.execute(sql)

        return {'message': 'The product was successfully deleted'}

    @staticmethod
    def open_connection():
        """opens up a connection to the database"""
        try:
            if os.environ.get('APP_SETTINGS') == 'testing':
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
