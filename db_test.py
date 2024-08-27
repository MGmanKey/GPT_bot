import sqlite3

conn = sqlite3.connect('db1.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (user_id INTEGER PRIMARY KEY, user_name TEXT, user_surname TEXT, username TEXT, timee TEXT)''')


user_id = 539937958
cursor.execute('SELECT timee FROM users WHERE user_id=?', (user_id,))
result = cursor.fetchone()[0].split()[1]
print(result)