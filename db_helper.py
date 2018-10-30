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
        self.all_sales = []
        self.conn = DBHelper.open_connection()
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def insert_record(self, record):
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
                {}({}, {}, {}, {}, {})
                VALUES('{}', '{}', '{}', '{}', '{}')
                """.format(
                        self.table_name,
                        self.table_fields[1],
                        self.table_fields[2],
                        self.table_fields[3],
                        self.table_fields[4],
                        self.table_fields[5],
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4]
                    )
            self.cur.execute(sql)
            message = "{} successfully created".format(record[0])

        # if self.table_fields[0] == 'sales_id':
        #     sql = """INSERT INTO 
        #     {}({}, {})
        #     VALUES('{}', '{}')
        #     """.format(
        #         self.table_name,
        #         self.table_fields[2],
        #         self.table_fields[3],
        #         record[1],
        #         record[2])
        #     self.cur.execute(sql)

        #     #get the id of the just created record
        #     sql_for_all_sales = """SELECT * FROM {}""".format(self.table_name)
        #     self.cur.execute(sql_for_all_sales)
        #     self.all_sales = self.cur.fetchall()

        #     # sql_for_id = """
        #     #         SELECT currval(pg_get_serial_sequence('{}', '{}'))
        #     #       """.format(self.table_name, self.table_fields[0])
        #     # self.cur.execute(sql_for_id)
        #     # result = self.cur.fetchone()

        #     # for product in record[0]:
        #     #     sql_for_products = """INSERT INTO 
        #     #                         sales_products(sale_id, product_details)
        #     #                             VALUES('{}', '{}')
        #     #                        """.format(result, product)
        #     #     self.cur.execute(sql_for_products)
        #     # message = "{} successfully created".format(record[0])

        # return self.all_sales

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

new_helper = DBHelper('sales', ['sale_id', 'product_details', 'total_amount', 'user_id'])
print(new_helper.insert_record([[{1: 300.00}, {2: 200.00}], 546.50, 1]))