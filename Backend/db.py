# db.py - PostgreSQL Version (Migrated from SQLite)
 
import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
 

load_dotenv()
 

DATABASE_URL = os.getenv("DATABASE_URL")
 

if not DATABASE_URL:
    raise ValueError(
        " DATABASE_URL environment variable not set.\n"
        "   On Render: Add DATABASE_URL in Settings → Environment\n"
        "   Locally: Create .env file with: DATABASE_URL=postgresql://..."
    )
 

try:
    conn_pool = SimpleConnectionPool(1, 20, DATABASE_URL)
except Exception as e:
    print(f" PostgreSQL connection error: {e}")
    conn_pool = None
 
 
def get_connection():
    """Get a database connection from the pool"""
    if not conn_pool:
        raise Exception(" Database connection pool not initialized")
    return conn_pool.getconn()
 
 
def release_connection(conn):
    """Release a connection back to the pool"""
    if conn_pool:
        conn_pool.putconn(conn)
 
 
def create_tables():
    """Create all tables in PostgreSQL"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
    
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            user_name VARCHAR(255) UNIQUE NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
 
      
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            query TEXT NOT NULL,
            title TEXT NOT NULL,
            link TEXT NOT NULL,
            year INTEGER,
            citations INTEGER,
            source VARCHAR(100) NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY(user_id) REFERENCES students(id),
            UNIQUE(user_id, title)
        )
        """)
 
       
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
 
        conn.commit()
        print(" Tables created successfully")
 
    except Exception as e:
        print(f" Error creating tables: {e}")
        conn.rollback()
    finally:
        release_connection(conn)
 
 
def insert_student(user_name):
    """Insert new student and return their ID"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute(
            "INSERT INTO students (user_name) VALUES (%s) RETURNING id",
            (user_name,)
        )
        student_id = cursor.fetchone()[0]
        conn.commit()
        return student_id
 
    except psycopg2.IntegrityError:
        
        conn.rollback()
        return get_student_id(user_name)
    except Exception as e:
        print(f" Error inserting student: {e}")
        conn.rollback()
        return None
    finally:
        release_connection(conn)
 
 
def get_student_id(user_name):
    """Get student ID by username"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute(
            "SELECT id FROM students WHERE user_name = %s",
            (user_name,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
 
    except Exception as e:
        print(f" Error getting student ID: {e}")
        return None
    finally:
        release_connection(conn)
 
 
def save_papers(user_id, query, papers):
    """Save multiple papers for a user"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        for paper in papers:
            title = paper.get("title", "")
            link = paper.get("link", "")
            year = paper.get("year", 0)
            citations = paper.get("citations", 0)
            source = paper.get("source", "openalex")
 
            try:
                cursor.execute("""
                    INSERT INTO papers (user_id, query, title, link, year, citations, source)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    query,
                    title,
                    link,
                    year,
                    citations,
                    source
                ))
 
            except psycopg2.IntegrityError:
                
                conn.rollback()
                continue
 
        conn.commit()
 
    except Exception as e:
        print(f" Error saving papers: {e}")
        conn.rollback()
    finally:
        release_connection(conn)
 
 
def get_papers_by_query(query):
    """Get all papers from a specific search query"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute("""
        SELECT title, link, year, citations, source
        FROM papers
        WHERE query = %s
        ORDER BY year DESC
        """, (query,))
 
        results = cursor.fetchall()
 
        # Convert tuples to dicts
        papers = []
        for row in results:
            papers.append({
                "title": row[0],
                "link": row[1],
                "year": row[2],
                "citations": row[3],
                "source": row[4]
            })
 
        return papers
 
    except Exception as e:
        print(f" Error getting papers by query: {e}")
        return []
    finally:
        release_connection(conn)
 
 
def get_papers_by_user(user_id):
    """Get all papers saved by a user"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute("""
        SELECT id, title, link, year, citations, source
        FROM papers
        WHERE user_id = %s
        ORDER BY date DESC
        """, (user_id,))
 
        results = cursor.fetchall()
 
        # Convert tuples to dicts
        papers = []
        for row in results:
            papers.append({
                "id": row[0],
                "title": row[1],
                "link": row[2],
                "year": row[3],
                "citations": row[4],
                "source": row[5]
            })
 
        return papers if papers else []
 
    except Exception as e:
        print(f" Error getting papers by user: {e}")
        return []
    finally:
        release_connection(conn)
 
 
def insert_search_history(query):
    """Log a search query"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute(
            "INSERT INTO search_history (query) VALUES (%s) RETURNING id",
            (query,)
        )
        history_id = cursor.fetchone()[0]
        conn.commit()
        return history_id
 
    except Exception as e:
        print(f" Error inserting search history: {e}")
        conn.rollback()
        return None
    finally:
        release_connection(conn)
 
 
def get_all_students():
    """Get all students (for debugging/admin)"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute("SELECT id, user_name, date FROM students ORDER BY date ASC")
        results = cursor.fetchall()
 
        students = []
        for row in results:
            students.append({
                "id": row[0],
                "user_name": row[1],
                "date": row[2]
            })
 
        return students
 
    except Exception as e:
        print(f" Error getting all students: {e}")
        return []
    finally:
        release_connection(conn)
 
 
def get_all_papers():
    """Get all papers (for debugging/admin)"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute("""
        SELECT title, link, year, citations, source
        FROM papers
        ORDER BY date ASC
        """)
 
        results = cursor.fetchall()
 
        papers = []
        for row in results:
            papers.append({
                "title": row[0],
                "link": row[1],
                "year": row[2],
                "citations": row[3],
                "source": row[4]
            })
 
        return papers
 
    except Exception as e:
        print(f" Error getting all papers: {e}")
        return []
    finally:
        release_connection(conn)
 
 
def get_all_search_history():
    """Get all search history (for debugging/admin)"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute("SELECT id, query, date FROM search_history ORDER BY date ASC")
        results = cursor.fetchall()
 
        history = []
        for row in results:
            history.append({
                "id": row[0],
                "query": row[1],
                "date": row[2]
            })
 
        return history
 
    except Exception as e:
        print(f" Error getting search history: {e}")
        return []
    finally:
        release_connection(conn)
 
 
def delete_paper_by_id(paper_id):
    """Delete a paper by ID"""
    conn = get_connection()
    cursor = conn.cursor()
 
    try:
        cursor.execute("DELETE FROM papers WHERE id = %s", (paper_id,))
        conn.commit()
 
    except Exception as e:
        print(f" Error deleting paper: {e}")
        conn.rollback()
    finally:
        release_connection(conn)
 