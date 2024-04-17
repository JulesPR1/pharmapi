import sqlite3

class DBQuery: 
  @staticmethod
  def create_drugs_table():
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        details_url TEXT,
        uses TEXT,
        side_effects TEXT,
        warnings TEXT,
        precautions TEXT,
        interactions TEXT,
        overdose TEXT
      )
    ''')
    connection.commit()
    connection.close()
  
  def clean_table(table):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    
    if not DBQuery.check_if_table_exists(table):
      connection.close()
      return False
    
    cursor.execute(f'''
      DELETE FROM {table}
    ''')
    connection.commit()
    connection.close()
  
  @staticmethod
  def insert(item, table):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    
    binder = []
    for i in range(len(item.keys())):
      binder.append('?')
      
    binder = ', '.join(binder)
    columns_names = ', '.join(item.keys())
    
    if not DBQuery.check_if_table_exists(table):
      connection.close()
      return False
    
    cursor.execute(f'''
      INSERT INTO {table} ({columns_names}) VALUES ({binder})
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
  def get_all(table):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    
    if not DBQuery.check_if_table_exists(table):
      return []
    
    cursor.execute(f'''
      SELECT * FROM {table}
    ''')
    
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    connection.close()

    result_dicts = [dict(zip(columns, row)) for row in results]

    return result_dicts
  
  @staticmethod
  def get_by_column(column, input):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    
    cursor.execute(f'''
      SELECT * FROM drugs WHERE {column} = ?
    ''', (input,))
    
    columns = [col[0] for col in cursor.description]
    results = cursor.fetchall()
    
    connection.close()
    
    result_dicts = [dict(zip(columns, row)) for row in results]
    return result_dicts
  
  @staticmethod
  def check_if_table_exists(table:str):
    connection = DBQuery.__get_connection()
    cursor = connection.cursor()
    
    cursor.execute(f'''
      SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'
    ''')
    
    if not cursor.fetchone():
      return False
    
    return True
  
  @staticmethod
  def __get_connection():
    return sqlite3.connect('app/database/db.sqlite3')
