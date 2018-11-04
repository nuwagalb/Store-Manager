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

        if self.table_fields[0] == 'user_id':
            sql = """INSERT INTO 
                {}({}, {}, {})
                VALUES('{}', '{}', '{}')
                RETURNING {}
                """.format(
                        self.table_name,
                        self.table_fields[1],
                        self.table_fields[2],
                        self.table_fields[3],
                        record[0],
                        record[1],
                        record[2],
                        self.table_fields[0]
                    )
            self.cur.execute(sql)
            result = self.cur.fetchone()

        if self.table_fields[0] == 'category_id':
            sql = """INSERT INTO 
                {}({})
                VALUES('{}', '{}')
                RETURNING {}
                """.format(
                        self.table_name,
                        self.table_fields[1],
                        record[0],
                        record[1],
                        self.table_fields[0]
                    )
            self.cur.execute(sql)
            result = self.cur.fetchone()

        if self.table_fields[0] == 'product_id':
            sql = """INSERT INTO 
                {}({}, {}, {})
                VALUES('{}', '{}', '{}')
                RETURNING {}
                """.format(
                        self.table_name,
                        self.table_fields[1],
                        self.table_fields[2],
                        self.table_fields[3],
                        record[0],
                        record[1],
                        record[2],
                        self.table_fields[0]
                    )
            self.cur.execute(sql)
            result = self.cur.fetchone()

        if self.table_fields[0] == 'sale_id':
            sql = """INSERT INTO 
                    {}({}, {}, {}, {})
                    VALUES('{}', '{}', '{}', '{}')
                    RETURNING {}
            """.format(
                self.table_name,
                self.table_fields[1],
                self.table_fields[2],
                self.table_fields[3],
                self.table_fields[4],
                record[0],
                record[1],
                record[2],
                record[3],
                self.table_fields[0]
            )
            self.cur.execute(sql)
            result = self.cur.fetchone()

        return result

    def find_record(self, value):
        """finds a record by a given value"""       
        sql = """SELECT * 
                 FROM {} 
                 WHERE {} = '{}'
              """.format(self.table_name, self.table_fields[1], value)
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
                RETURNING {}
            """.format(
                self.table_name,
                field_name,
                name_value,
                field_id,
                id_value,
                self.table_fields[0])
        self.cur.execute(sql)
        updated_rows = self.cur.rowcount

        return updated_rows

    def delete_record(self, record_id):
        """deletes a record from the database"""
        sql = """DELETE
                 FROM {} 
                 WHERE {} = {}
                 RETURNING {}
              """.format(
                  self.table_name,
                  self.table_fields[0],
                  record_id,
                  self.table_fields[1])

        self.cur.execute(sql)
        deleted_name = self.cur.fetchone()

        return deleted_name

    @staticmethod
    def open_connection():
        """opens up a connection to the database"""
        try:
            if os.environ.get('APP_SETTINGS') == 'testing':
                db_name = test_db_name
            elif os.environ.get('DATABASE_URL') == 'heroku':
                db_name = os.environ['DATABASE_URL']
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
