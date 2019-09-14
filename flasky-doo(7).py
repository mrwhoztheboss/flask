from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!!</h1>'

@app.route('/home', methods=['POST', 'GET'], defaults={ 'name' : 'Default' })
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
	return '<h1>Hello {}, you are on the Home Page!!</h1>'.format(name)

@app.route('/json')
def json():
	return jsonify({ 'key' : 'value', 'listkeys' : [1,2,3] })

@app.route('/query')
def query():
	name = request.args.get('name')
	loc = request.args.get('loc')
	return '<h1>Hello <font color="red">{}</font> from <font color="red">{}</font>, you are on the Query Page!!</h1>'.format(name,loc)

@app.route('/theform')
def theform():
    return '''<form method="POST" action="/process">
                  <input type="text" name="name">
                  <input type="text" name="loc">
                  <input type="submit" value="Submit">
              </form>'''

@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    loc = request.form['loc']
    return '<h1>Hello <font color="red">{}</font> from <font color="red">{}</font>. You have submitted the form successfully!<h1>'.format(name, loc)

if __name__ == '__main__':
	app.run(debug = True)