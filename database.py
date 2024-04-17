import psycopg2
from flask import Flask
import multiprocessing

app = Flask(__name__)

class UserInfo:
    def __init__(self, tracking_stocks, email_sms_value, timer, selected_option, name, password):
        self.tracking_stocks = tracking_stocks
        self.email_sms_value = email_sms_value
        self.timer = timer
        self.selected_option = selected_option
        self.name = name
        self.password=password


def create_database(user_info):
    hostname = 'localhost'
    database = 'postgres'
    username = 'postgres'
    pswd = 'Cueva123'
    port_id = '5433'
    
    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pswd,
            port=port_id
        )
        
        cur = conn.cursor()

        # Extracting attributes from the UserInfo instance
        user_name = user_info.name
        user_email = user_info.email_sms_value
        user_membership = user_info.selected_option
        user_stock = user_info.tracking_stocks
        user_password = user_info.password

        # Creating table if not exists
        create_table_query = '''CREATE TABLE IF NOT EXISTS Investiwatcher_users (
                                user_name VARCHAR(50),
                                user_email VARCHAR(50) PRIMARY KEY,
                                user_membership VARCHAR(20),
                                user_stock VARCHAR(20),
                                user_password VARCHAR(50)
                            )'''
        cur.execute(create_table_query)
        
        # Inserting user information into the table
        insert_query = "INSERT INTO Investiwatcher_users (user_name, user_email, user_membership, user_stock) VALUES (%s, %s, %s, %s)"
        cur.execute(insert_query, (user_name, user_email, user_membership, user_stock, user_password))
        
        conn.commit()

    except Exception as error:
        print(error)

    finally: 
        if cur is not None: 
            cur.close()
        if conn is not None:
            conn.close()



# Create an instance of UserInfo


# Call the create_database function with user_info
create_database(UserInfo)
