from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!!</h1>'

@app.route('/home', methods=['POST', 'GET'])
def home():
	return '<h1>You are on the Home Page!!</h1>'

@app.route('/json')
def json():
	return jsonify({ 'key' : 'value', 'listkeys' : [1,2,3] })

if __name__ == '__main__':
	app.run(debug = True)