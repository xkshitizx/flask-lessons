from flask import Flask,jsonify, request, url_for, redirect, session,render_template

app=Flask(__name__)

app.config['DEBUG'] = True #debug mode on
app.config['SECRET_KEY'] = 'thisisasecret'

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
@app.route('/theform')
def theform():
	return render_template('form.html', title="Register")
@app.route('/process', methods=["POST"])
def process():
	name=request.form['name']
	location = request.form["location"]

	return"hello {}. You are from {}".format(name,location)


if __name__== '__main__':
	app.run()

