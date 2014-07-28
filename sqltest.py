import sqlite3

conn = sqlite3.connect('app.db')
print('Opened DB Successfully')


# cursor = conn.execute('select * from query')



conn.execute("insert into user values(1, 'balazs.cseh', 'ticket', 1)")
conn.commit()

# for row in cursor.fetchall():
# 	print row


print('Query Execution Completed')

conn.close()
