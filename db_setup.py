import psycopg2
from db_config import prod_db_name, db_host, db_user, db_password, db_port, test_db_name
import os
class Database:
    """
       class to handle database connections
    """

    def default_connection(self):
        """set up default connection to create the sepicified database"""
        try:
            if os.getenv('APP_SETTING') == 'testing':
                db_name = test_db_name
            else:
                db_name = prod_db_name

            connection = psycopg2.connect("dbname={} host={} user={} password={} port={}".format(
                'postgres', db_host, db_user, db_password, db_port))
            connection.autocommit = True
            cursor = connection.cursor()

            database_existance_sql = """SELECT COUNT(*) = 0 
                                        FROM pg_catalog.pg_database 
                                        WHERE datname = '{}'""".format(db_name)

            cursor.execute(database_existance_sql)
            db_result = cursor.fetchone()
            
            if db_result[0]:
                cursor.execute('CREATE DATABASE {}'.format(db_name))
                print("Database {} successfully created".format(db_name))
                connection.close()
            else:
                print("Database {} already exists".format(db_name))
                return False

        except psycopg2.Error as error:
            print(error)

        finally:
            connection.close()      
        return True

    def connection_to_create_tables(self):
        """sets up connection for creating tables inside the specified database"""
        try:
            if self.default_connection() is True:

                if os.getenv('APP_SETTING') == 'testing':
                    db_name = test_db_name
                else:
                    db_name = prod_db_name
                    
                connection = psycopg2.connect("dbname={} host={} user={} password={} port={}".format(
                    db_name, db_host, db_user, db_password, db_port))
                connection.autocommit = True
                cursor = connection.cursor()

                user_sql = """CREATE TABLE IF NOT EXISTS users(
                        user_id serial PRIMARY KEY,
                        email VARCHAR (355) UNIQUE NOT NULL,
                        password VARCHAR (350) NOT NULL,
                        role VARCHAR(50) NOT NULL,
                        date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        date_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );"""
                cursor.execute(user_sql)

                category_sql = """CREATE TABLE IF NOT EXISTS categories(
                        category_id serial PRIMARY KEY,
                        name VARCHAR (250) NOT NULL,
                        date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        date_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    );"""

                cursor.execute(category_sql)

                product_sql = """CREATE TABLE IF NOT EXISTS products(
                                product_id serial PRIMARY KEY,
                                name VARCHAR (250) NOT NULL,
                                unit_price NUMERIC(11, 4) NOT NULL,
                                quantity NUMERIC(11, 4) NOT NULL,
                                category_id INT NULL, FOREIGN KEY (category_id) REFERENCES categories(category_id),
                                date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                date_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                            );"""
                cursor.execute(product_sql)
            
                sales_sql = """CREATE TABLE IF NOT EXISTS sales(
                                sale_id serial PRIMARY KEY,
                                total_amount NUMERIC(11, 4) NOT NULL,
                                user_id INT NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id),
                                date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                date_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                            );"""
                cursor.execute(sales_sql)

                sales_products_sql = """CREATE TABLE IF NOT EXISTS sales_products(
                                sale_product_id serial PRIMARY KEY,
                                sale_id INT NOT NULL, FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
                                product_details VARCHAR(250) NOT NULL,
                                date_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                date_modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                            );"""
                cursor.execute(sales_products_sql)

                connection.close()

                return "Tables were successfully created"

            return "Tables could not be created"

        except psycopg2.Error as error:
            print(error)

#instance for creating database and tables
db = Database()
print(db.connection_to_create_tables())
