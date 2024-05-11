import sqlite3
import datetime

def add_data(temperatura, umiditate):
    conn = sqlite3.connect('airParameters.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parametrii (
            id INTEGER PRIMARY KEY,
            temperatura REAL,
            umiditate REAL,
            timp TEXT
        )
    ''')

    timp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('INSERT INTO parametrii (temperatura, umiditate, timp) VALUES (?, ?, ?)', (temperatura, umiditate, timp))
    conn.commit()
    conn.close()
