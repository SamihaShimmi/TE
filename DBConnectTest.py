import os
import sqlite3
'''
try:
    os.remove("TestEvolutionDB.db")
    conn = sqlite3.connect('TestEvolutionDB.db')
except FileNotFoundError:
    conn = sqlite3.connect('TestEvolutionDB.db')
'''
conn = sqlite3.connect('TestEvolutionDB.db')
cur = conn.cursor()

insertValues = ['s', 'ss', 'path','ssss']

conn.execute("INSERT INTO dataset VALUES (?,?,?,?)", insertValues)

'''
t1 = "CREATE TABLE t(x INTEGER)"
conn.execute(t1)
'''
for row in cur.execute('select path from dataset'):
    print (row)
conn.commit()
conn.close()