'''module to handle all sqlite related functions '''
##important modules 
import sqlite3 # for data recording 
import calendar # for time and take 
from datetime import datetime # for time and take
import pickle # for serialization 


# Connect to SQLite database (or create it if it doesn't exist)

#making it a function 
def database_connect():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Create a table to store serialized objects
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS good_habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        object BLOB
               
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bad_habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        object BLOB
               
    )''')
    conn.commit()

'''functions to load the data to and from the database'''


def save_object_to_db(obj,table):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    name=obj.name #for easy of seaching of habits in the database 
    serialized_data = serialize_object(obj)
    cursor.execute(f'INSERT OR REPLACE INTO {table} (name,object) VALUES (?,?)', (name,serialized_data,))
    conn.commit()

def load_object_from_db1(name,table):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE name = ?",(name,))
    result = cursor.fetchone()
    if result:
        #print(result)
        serialized_data = result[2]#here were mostly interested in the object from the data base 
        a=deserialize_object(serialized_data)
        return a
    return None

## to handle the deleting of habits from out database
def delete_habit_from_database(name,table):
    conn= sqlite3.connect('my_database.db')
    cursor=conn.cursor()
    cursor.execute(f"DELETE FROM {table} where name = ?",(name,))
    conn.commit()
    if not None:
        return f"habit:{name}, is deleted from our records " 


# to handle selecting all objects from the database 
def select_all(table_name):
    conn= sqlite3.connect('my_database.db')
    cursor=conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    objects=[]
    result=cursor.fetchall()
    if result:
        ## replace the object with a deserialized one 
        
        for i in result:
            row=[]
            row.append(i[0])
            row.append(deserialize_object(i[2]))
            objects.append(row)
        
    return objects
def update_habit(habit_name,habit_object,table_name):
    conn= sqlite3.connect('my_database.db')
    cursor=conn.cursor()
    update_query = f"UPDATE {table_name} SET object = ? WHERE name = ?"
    data = (serialize_object(habit_object), habit_name) #updating the object column 
    cursor.execute(update_query, data)
    conn.commit()



'''functions to serialize the data and deserialize the data'''
def serialize_object(obj):
    return pickle.dumps(obj)

def deserialize_object(serialized_data):
    return pickle.loads(serialized_data)

'''funtion to truncate the table '''
def truncate(TABLE):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    
    cursor.execute(f'DELETE FROM {TABLE}')
    
    conn.commit()