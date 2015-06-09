import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='bank.db'):
	new = not os.path.exists(path)
	db = sqlite3.connect(path)
	if new :
		c = db.cursor()
		c.execute('CREATE TABLE payment (id INTEGER PRIMARY KEY,'
				  ' name TEXT, password TEXT, dollars TEXT, memo TEXT)')
		add_payment(db, 'apple', '123', 100, 'this is apple')
		add_payment(db, 'banana', '1234', 1000, 'this is banana')
		add_payment(db, 'cat', '12345', 10000, 'this is cat')
		db.commit()
	return db

def add_payment(db, name, password, dollars, memo):   #  db, TEXT, TEXT, TEXT, TEXT
	db.cursor().execute('INSERT INTO payment (name, password, dollars, memo)'
						' VALUES (?,?,?,?)', (name, password, dollars, memo))

					

def get_payments_of(db,name,password):
	c = db.cursor()
	
	# update information
	#c.execute('UPDATE payment SET dollars = ? , memo = ?'
	#		  ' WHERE debit = ? and credit = ?', ("12345","this is memo","brandon", "psf"))	  
	#db.commit()
	
	c.execute('SELECT * FROM payment WHERE name = ? or password = ?'
			  ' ORDER BY id', (name, password))

	Row = namedtuple('Row', [tup[0] for tup in c.description])
	return [Row(*row) for row in c.fetchall()]
	
if __name__ == '__main__':
	db = open_database()
	pprint.pprint(get_payments_of(db, 'apple', '123'))
	pprint.pprint(get_payments_of(db, 'banana', '1234'))
	pprint.pprint(get_payments_of(db, 'cat', '12345'))

	