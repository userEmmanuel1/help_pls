import psycopg2
from flask import Flask
import multiprocessing

#THE SCRIPT START SO THE PROBLEM IS UNPACKING DATA FROM CREATE_DATABASE ANF PASSING TO POSTGRES

app = Flask(__name__)
print("THE DATBASE.PY SCRIPT WORKS")

user_info = None

def set_user_info(info):
    global user_info
    user_info = info

def create_database():
    global user_info
    
    # Use the user_info global variable here to access the data

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="Cueva123", port="5433")
        cur = conn.cursor() 

        # Extracting attributes from the user_info instance
        user_name = user_info.name
        user_email = user_info.email_sms_value
        user_membership = user_info.selected_option
        user_stock = user_info.tracking_stocks

       

        # Creating table if not exists
        create_table_query = '''CREATE TABLE IF NOT EXISTS Investiwatcher_users (
                                user_name VARCHAR(50),
                                user_email VARCHAR(50) PRIMARY KEY,
                                user_membership VARCHAR(20),
                                user_stock VARCHAR(20)
                            )'''
        cur.execute(create_table_query)
        
        # Inserting user information into the table
        insert_query = "INSERT INTO Investiwatcher_users (user_name, user_email, user_membership, user_stock) VALUES (%s, %s, %s, %s)"
        cur.execute(insert_query, (user_name, user_email, user_membership, user_stock))
        
        conn.commit()

    except Exception as error:
        print(error)

    finally: 
        if cur is not None: 
            cur.close()
        if conn is not None:
            conn.close()

print("THE DATBASE.PY SCRIPT WORKS")

# Create an instance of user_info


# Call the create_database function with user_info
#create_database(user_info(tracking_stocks, email_sms_value, timer, selected_option, name))
