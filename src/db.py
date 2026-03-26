import sqlite3

DB = "quickscholar.db"

# Function to create tables for students, papers, and search history
def create_tables():

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT UNIQUE NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP)

        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    citations INTEGER NOT NULL,
                    doi TEXT UNIQUE ,
                    abstract TEXT ,
                    full_text TEXT ,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    source TEXT NOT NULL)
                    """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP)
                        """)
        conn.commit()   
    

# Insert functions for students, papers, and search history
def insert_student(user_name):

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (user_name) VALUES(?)", (user_name,))

        conn.commit()
        return cursor.lastrowid
    


def insert_paper(title, year, citations, doi, abstract, full_text, source):

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO papers (title, year, citations, doi, abstract, full_text, source) VALUES(?,?,?,?,?,?,?)", 
                    (title, year, citations, doi, abstract, full_text, source))
        
        conn.commit()
        return cursor.lastrowid

def insert_search_history(query):

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO search_history (query) VALUES(?)", (query,))

        conn.commit()
        return cursor.lastrowid

# Get functions for students, papers, and search history
def get_all_students():

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM students ORDER BY date ASC")
        return [dict(row) for row in cursor.fetchall()]

    conn.commit()

    

def get_all_papers():

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM papers ORDER BY date ASC")
        return [dict(row) for row in cursor.fetchall()]
    conn.commit()

def get_all_search_history():

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM search_history ORDER BY date ASC")
        return [dict(row) for row in cursor.fetchall()]
    conn.commit()



    
