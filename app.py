from flask import Flask,jsonify, request, url_for, redirect, session,render_template,g, redirect #global object that allows to store data 
import sqlite3

app=Flask(__name__)

app.config['DEBUG'] = True #debug mode on
app.config['SECRET_KEY'] = 'thisisasecret'

def connect_db():
	'''function to connect with database'''

	sql = sqlite3.connect('data.db') #connecting
	sql.row_factory = sqlite3.Row #change tuple into dictionary which is tuple by default
	return sql

def get_db():
	'''function to get database'''
	if not hasattr(g, 'sqlite3'): #check if database is already there
		g.sqlite_db = connect_db() #add connection
	return g.sqlite_db

@app.teardown_appcontext #automatically called when route returns
def close_db(error):
	'''close connection to the database automatically after executing every routes'''
	if hasattr(g,'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def index():
	session.pop('name',None)
	return "<h1>Hello world!!</h1>"


@app.route('/home',methods=['GET', 'POST'], defaults = {'name': 'User'})
@app.route('/home/<string:name>') #adding parameter as url with type
def home(name):
	session['name']=name
	my_list = [1,2,3,4,5,6,7]
	person={'name': 'Kshitiz',
			'class': 18,
			'section': 'D'}
	title = f"{name.title()}'s page"
	return render_template('home.html',title=title, name=name, display=False, list=my_list, dict=person)

'''adding http request method'''
@app.route('/json',methods=['POST','GET'])
def json():
	if 'name' in session:
		name = session['name']
	else:
		name="NotInSession"
	return jsonify({'key': 'value','key2':[1,2,3],'name':name})

'''request query string'''
@app.route('/query')
def query():
	name = request.args.get('name')
	location = request.args.get('location')
	return '<h1>hi {}, You are from {} </h1>'.format(name,location)

#request form data
@app.route('/theform', methods=['GET', 'POST'])
def theform():
	if request.method == 'GET':
		return render_template('form.html', title="Register")
	else:
		name = request.form['name']
		location = request.form['location']
		print(f"{name}{location}")
		db = get_db()
		db.execute('insert into users (name, location) values (?, ?)',[ name, location])
		db.commit()
		oneid = db.execute('select id from users where name=? and location=?',[name,location]).first()
		id = oneid.first()
		return redirect(url_for('justmade'),id=id)

# @app.route('/process', methods=["POST"])
# def process():
# 	name=request.form['name']
# 	location = request.form["location"]

# 	return"hello {}. You are from {}".format(name,location)

#get the results from database using query
@app.route('/viewone/<integer:id>', methods=['GET'])
def viewone():
	db = get_db()
	id = request.url
	point = db.execute('select name,location from users where id=?',[id])
	return render_template('justmade.html',name=name,location=location)


@app.route('/viewresults',methods=['POST','GET'])
def viewresults(): #r in crud
	db = get_db()
	cur = db.execute('select id,name,location from users')
	results = cur.fetchall()
	 #fetch list of dictionaries from cu
	return render_template('viewresults.html',users=results)

if __name__== '__main__':
	app.run()

