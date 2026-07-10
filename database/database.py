import sqlite3

DATABASE_NAME = "database/prompt_history.db"


def create_database():
    """
    Creates the SQLite database and history table.
    """

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt_title TEXT,
        prompt TEXT,
        response TEXT,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_history(prompt_title, prompt, response, score):
    """
    Save one prompt comparison to the database.
    """

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history(prompt_title, prompt, response, score)
    VALUES (?, ?, ?, ?)
    """, (prompt_title, prompt, response, score))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        created_at,
        prompt_title,
        score
    FROM history
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def get_statistics():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        COUNT(*),
        MAX(score),
        AVG(score),
        MIN(score)
    FROM history
    """)

    stats = cursor.fetchone()

    conn.close()

    return stats

def get_score_history():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        prompt_title,
        score,
        created_at
    FROM history
    ORDER BY id ASC
    """)

    data = cursor.fetchall()

    conn.close()

    return data