# Db.py


import sqlite3

DB = "quickscholar.db"



def create_tables():

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL,            
            year INTEGER,
            citations INTEGER,
            source TEXT NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

  
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()



def save_papers(query, papers):

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()

        for paper in papers:
            title = paper.get("title", "")
            link = paper.get("link", "")        
            year = paper.get("year", 0)
            citations = paper.get("citations", 0)
            source = paper.get("source", "openalex")

            try:
                cursor.execute("""
                    INSERT INTO papers(query, title, link, year, citations, source)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    query,
                    title,
                    link,
                    year,
                    citations,
                    source
                ))

            except sqlite3.IntegrityError:
                continue

        conn.commit()



def get_papers_by_query(query):

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()


        cursor.execute("""
        SELECT title, link, year, citations, source
        FROM papers
        WHERE query = ?
        ORDER BY year DESC
        """, (query,))

        results = cursor.fetchall()

        return [dict(row) for row in results] if results else None



def insert_student(user_name):

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO students (user_name) VALUES(?)",
            (user_name,)
        )

        conn.commit()
        return cursor.lastrowid





def insert_search_history(query):

    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO search_history (query) VALUES(?)",
            (query,)
        )

        conn.commit()
        return cursor.lastrowid



def get_all_students():

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students ORDER BY date ASC")
        return [dict(row) for row in cursor.fetchall()]


def get_all_papers():

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
        SELECT title, link, year, citations, source
        FROM papers
        ORDER BY date ASC
        """)

        return [dict(row) for row in cursor.fetchall()]


def get_all_search_history():

    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM search_history ORDER BY date ASC")
        return [dict(row) for row in cursor.fetchall()]
