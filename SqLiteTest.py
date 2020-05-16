import sqlite3

conn = sqlite3.connect("a.db3")
# conn = sqlite3.connect(":memory:")

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS test (
		name text,
		number integer
	)""")

for i in range(10):
	with conn:
		c.execute("INSERT INTO test (name, number) VALUES (?, ?)", ("A" + str(i), i))
		c.execute("INSERT INTO test (name, number) VALUES (:name, :num)", 
			{ "name": "A" + str(i * i), "num": i * i})

c.execute("SELECT name, number FROM test WHERE number % 2 = 1")

while True:
	record = c.fetchone()
	if record == None:
		break;
	print(record)

conn.commit()
conn.close()
