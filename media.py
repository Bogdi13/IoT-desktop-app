import sqlite3
from datetime import datetime, timedelta

def medii_24h():
    conn = sqlite3.connect('airParameters.db')
    cursor = conn.cursor()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    cursor.execute('SELECT * FROM parametrii WHERE timp BETWEEN ? AND ?', (start_time, end_time,))
    rows = cursor.fetchall()
    sum_temp = 0
    sum_umid = 0
    count = len(rows)
    for row in rows:
        sum_temp += row[1]
        sum_umid += row[2]

    media_temp = sum_temp / count
    media_umid = sum_umid / count

    conn.close()

    return media_temp, media_umid


def medii_1h():
    conn = sqlite3.connect('airParameters.db')
    cursor = conn.cursor()
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    cursor.execute('SELECT * FROM parametrii WHERE timp BETWEEN ? AND ?', (start_time, end_time,))
    rows = cursor.fetchall()
    sum_temp = 0
    sum_umid = 0
    count = len(rows)
    for row in rows:
        sum_temp += row[1]
        sum_umid += row[2]

    media_temp = sum_temp / count
    media_umid = sum_umid / count

    conn.close()

    return media_temp, media_umid