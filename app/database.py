import sqlite3

#Open database
conn = sqlite3.connect('/Users/raj.burad7/Desktop/APMiniProject2/app/site.db')

#Create table
c=conn.cursor()

# conn.execute("ALTER TABLE user ADD type TEXT ")
conn.execute('''CREATE TABLE flights
		(flightid INTEGER PRIMARY KEY,
		destination TEXT,
		arrival TEXT,
		airlines TEXT,
		flightno TEXT,
        depart TEXT,
        arrive TEXT,
        duration TEXT,
        type TEXT,
        price INTEGER
		)''')




                
                

conn.close()


