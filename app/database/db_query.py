import sqlite3

class DBQuery: 
  @staticmethod
  def create_table():
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        details_url TEXT,
        uses TEXT,
        side_effects TEXT,
        precautions TEXT,
        interactions TEXT,
        overdose TEXT
      )
    ''')
    connection.commit()
    connection.close()
  
  def clean_table(table_name):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    cursor.execute(f'''
      DELETE FROM  {table_name}
    ''')
    connection.commit()
    connection.close()
  
  @staticmethod
  def insert(item, table_name):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    
    binder = []
    for i in range(len(item.keys())):
      binder.append('?')
      
    binder = ', '.join(binder)
    columns_names = ', '.join(item.keys())
    
    cursor.execute(f'''
      INSERT INTO {table_name} ({columns_names}) VALUES ({binder})
    ''', list(item.values()))
    connection.commit()
    connection.close()
    
  @staticmethod
  def get_tables_names():
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    cursor.execute('''
      SELECT name FROM sqlite_master WHERE type='table'
    ''')
    tables = cursor.fetchall()
    connection.close()
    return tables
  
  @staticmethod
  def __get_connection():
    return sqlite3.connect('database/db.sqlite3')
