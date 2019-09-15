from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'ThisIsASecret'

def connect_db():
	sql = sqlite3.connect('C:/Users/Mitesh Vishwasrao/Documents/flask_app/data.db')
	sql.row_factory = sqlite3.Row
	return sql

def get_db():
	if not hasattr(g, 'sqlite3'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

@app.route('/')
def index():
	session.pop('name', None)
	return '<h1>Hello World!!</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={ 'name' : 'Default' })
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
	session['name'] = name
	db = get_db()
	cur = db.execute('select id, name, location from users')
	results = cur.fetchall()
	return render_template('home.html', name=name, display=True, mylist=[1,2,3], \
		lod=[{'name':'Zack'}, {'name':'Zoe'}], results=results)

@app.route('/json')
def json():
	if 'name' in session:
		name = session['name']
	else:
		name = 'NotInSession'
	return jsonify({ 'key' : 'value', 'listkeys' : [1,2,3], 'name' : name })

@app.route('/query')
def query():
	name = request.args.get('name')
	loc = request.args.get('loc')
	return '<h1>Hello <font color="red">{}</font> from <font color="red">{}</font>, you are on the Query Page!!</h1>'.format(name,loc)

@app.route('/theform', methods=['GET', 'POST'])
def theform():
	if request.method == 'GET':
		return render_template('form.html')
	else:
		name = request.form['name']
		location = request.form['location']
		db = get_db()
		db.execute('insert into users (name, location) values (?, ?)', [name, location])
		db.commit()
	return '<h1>Hello {} from {}. You have submitted the form successfully!<h1>'.format(name, location)

'''@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    loc = request.form['loc']
    return '<h1>Hello {} from {}. You have submitted the form successfully!<h1>'.format(name, loc)'''

@app.route('/processjson', methods=['POST'])
def processjson():
    data = request.get_json()
    name = data['name']
    loc = data['loc']
    randomlist = data['randomlist']
    return jsonify({'result' : 'Success!', 'name' : name, 'loc' : loc, 'randomkeyinlist' : randomlist[1]})


@app.route('/theformreform', methods=['GET', 'POST'])
def theformreform():
    if request.method == 'GET':
        return '''<form method="POST" action="/theformreform">
                      <input type="text" name="name">
                      <input type="text" name="loc">
                      <input type="submit" value="Submit">
                  </form>'''
    else:
        name = request.form['name']
        loc = request.form['loc']
        return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, loc)
'''
@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    location = request.form['location']

    return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
'''

@app.route('/theformredirect', methods=['GET', 'POST'])
def theformtourl():
    if request.method == 'GET':
        return '''<form method="POST" action="/theformtourl">
                      <input type="text" name="name">
                      <input type="text" name="loc">
                      <input type="submit" value="Submit">
                  </form>'''
    else:
        name = request.form['name']
        #loc = request.form['loc']
        #return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, loc)
        return redirect(url_for('home', name = name))

@app.route('/viewresults')
def viewresults():
	db = get_db()
	cur = db.execute('select * from users')
	results = cur.fetchall()
	return '<h1>The id is {} for {} who is from {}</h1>'.format(results[2]['id'], results[2]['name'], results[2]['location'])

if __name__ == '__main__':
	app.run()