import sqlite3

conn = sqlite3.connect('chatbox.db')
cur = conn.cursor()

# Tạo bảng messages
# cur.execute('''
# CREATE TABLE IF NOT EXISTS messages (
#     id_message INTEGER PRIMARY KEY AUTOINCREMENT,
#     sender TEXT NOT NULL,
#     message_content TEXT NOT NULL,
#     timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )
# ''')

# conn.commit()

cur.execute('SELECT * from messages')
i = cur.fetchall()

for i in i:
    print(i)
conn.close()
