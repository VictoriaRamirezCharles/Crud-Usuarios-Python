import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO usuarios (nombre, content) VALUES (?, ?)",
            ('Victoria', 'Prueba 1')
            )

cur.execute("INSERT INTO usuarios (nombre, content) VALUES (?, ?)",
            ('Alex', 'Prueba 2')
            )

connection.commit()
connection.close()