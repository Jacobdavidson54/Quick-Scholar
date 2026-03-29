# Db.py
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
                    query TEXT NOT NULL,  
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
    

def save_papers(query, papers):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        for paper in papers:
            title = paper.get("title", "Unknown Title")
            year = paper.get("year", 0)
            citations = paper.get("citations", 0)   
            doi = paper.get("doi", None)
            abstract = paper.get("abstract", "")
            full_text = paper.get("full_text", "")
            source = paper.get("source", "Unknown Source")

            try:
                cursor.execute("""
                    INSERT INTO papers(query, title, year, citations, doi, abstract, full_text, source)
                    VALUES (?,?,?,?,?,?,?,? )
                               """,(
                    query,
                    title,
                    year,
                    citations,
                    doi,
                    abstract,
                    full_text,
                    source
                    ))
                
            except sqlite3.IntegrityError:
                continue

        conn.commit()


def get_papers_by_query(query):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(("""
        SELECT * FROM papers
        WHERE query = ? 
        ORDER BY citations DESC
        """) ,(query,))

        results = cursor.fetchall()
        return [dict(row) for row in results] if results else None
    



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

  
