from init import e

e.execute("""
	create table malt (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		PPG REAL NOT NULL,
		Lovibond REAL NOT NULL
	)
""")

e.execute("""
	create table hop (
		id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
		Hop TEXT NOT NULL,
		AA REAL NOT NULL
	)
""")