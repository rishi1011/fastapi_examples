import sqlite3

conn = sqlite3.connect("mydb.db")
cursor = conn.cursor()

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL
)
"""
)

cursor.execute(
    """
INSERT INTO users (name, email)
VALUES
('The Pragmatic Programmer', '123@123.com'),
('Clean Code', '234@234.com'),
('Deep Learning with Python', '345@345.com')
"""
)

conn.commit()

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

for row in rows:
    print(row)
    
conn.close()
