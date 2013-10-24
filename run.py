from bottle import route, run, template, static_file
import os

@route('/')
def index():
    return send_static('index.html')

@route('/hello')
@route('/hello/<name>')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/static/<filename:path>')
def send_static(filename):
    print("loading /static/" + filename)
    return static_file(filename, os.getcwd() +  '/static/') 

run(host='localhost', port=8080)
