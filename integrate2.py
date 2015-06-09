import os, pprint, sqlite3
from collections import namedtuple
from flask import Flask
from flask import request
from flask import redirect
from OpenSSL import SSL

app = Flask(__name__)

@app.route('/')
def login():
	s = """
	<!DOCTYPE html>
	<html lang="en">
	<body>
		<h1>Enter some text</h1>
		<form action="https://127.0.0.1:12111/login" method="POST">
			Name : <input type="text" name="name"><br>
			Password : <input type="text" name="password"><br>
			<input type="submit" name="login" value="Send">
		</form>
	</body>
	</html>
	"""
	return s	
	
@app.route('/login', methods=['GET'])	
def login_get():
	if request.url == "https://127.0.0.1:12111/login":
		s = "You have not enter your name and password"
		return s	

@app.route('/login', methods=['POST'])
def login_post():
	Name = request.form['name']
	Password = request.form['password']
	check = checkValidUser(Name,Password)
	if check == True:
		s = "https://127.0.0.1:12111/page" + "?" + "name=" + Name + "&" + "password=" + Password
		return redirect(s)
	else:
		s = "Name or Password is wrong!"
		return s                        		   

		
@app.route('/page')
def page_post():
	if request.url == "https://127.0.0.1:12111/page":
		s = "You have not enter your name and password"
		return s
	
	a = request.args.get('name')
	b = request.args.get('password')
	userdata = showInWebsite(a,b)
	s = """
	<!DOCTYPE html>
	<html lang="en">
		User Data:<br>
	""" 
	s = s + userdata
	s = s + "<form action='https://127.0.0.1:12111/modify' method='POST'>"
	s = s + "Name : <input type='text' name='name' readonly value=" + a + "><br>"
	s = s + "Password : <input type='text' name='password' readonly value=" + b + "><br>"
	s = s + """
			dollars : <input type="text" name="dollars"><br>
			memo : <input type="text" name="memo"><br>
			<input type="submit" name="modify" value="Modify data">
		</form>
	</html>
	"""
	return s			

	
@app.route('/modify', methods=['GET'])	
def modify_get():
	if request.url == "https://127.0.0.1:12111/modify":
		s = "You have not enter your name and password"
		return s
	
	
@app.route('/modify', methods=['POST'])
def modify_post():	
	name = request.form['name']
	password = request.form['password']
	dollars = request.form['dollars']
	memo = request.form['memo']
	updateInformation(name,password,dollars,memo)
	s = "https://127.0.0.1:12111/page" + "?" + "name=" + name + "&" + "password=" + password
	return redirect(s)
	
	
def showInWebsite(name,password):
	c = db.cursor()
	c.execute('SELECT * FROM payment WHERE name = ? and password = ?', (name,password))
	returnObject = c.fetchone()
	s = "" + returnObject[1] + "," + returnObject[2] + "," + returnObject[3] + "," + returnObject[4]
	return s
	
	
def updateInformation(name,password,dollars,memo):
	c = db.cursor()
	if dollars != "":
		c.execute('UPDATE payment SET dollars = ? WHERE name = ?', (dollars,name))	  
	if memo != "":
		c.execute('UPDATE payment SET memo = ? WHERE name = ?', (memo,name))
	db.commit()
	pprint.pprint(showInCommand(name))
	
	
def checkValidUser(name,password):
	c = db.cursor()
	c.execute('SELECT * FROM payment WHERE name = ? and password = ?', (name, password))
	returnObject = c.fetchone()
	if returnObject:
		print(returnObject[0])
		print(returnObject[1])
		print(returnObject[2])
		print(returnObject[3])
		print(returnObject[4])
		return True
	else:
		print("Name or Password is wrong!")
		return False
	
	
def checkDataBase(path):
	old = os.path.exists(path)
	if old:
		print("{} database exist".format(path))
		return True
	else:
		print("{} database does not exist".format(path))
		return False
	
	
def showInCommand(name):
	c = db.cursor()
	c.execute('SELECT * FROM payment WHERE name = ?', (name,))
	Row = namedtuple('Row', [tup[0] for tup in c.description])
	return [Row(*row) for row in c.fetchall()]

	
if __name__ == "__main__":
	exist = checkDataBase('bank.db')
	if exist:
		global db
		db = sqlite3.connect('bank.db')
		pprint.pprint(showInCommand('apple'))
		pprint.pprint(showInCommand('banana'))
		pprint.pprint(showInCommand('cat'))
		#app.run()
		app.run('127.0.0.1', debug=False, port=12111, ssl_context='adhoc')