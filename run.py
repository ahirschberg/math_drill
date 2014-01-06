#!/usr/bin/env python3
import bottle
from bottle import *
import os
import random
import sys
import hashlib
import sqlite3
import re
import uuid


print(sys.argv)
dev = False
# If -l flag is used, run in python3 mode 
if (len(sys.argv) > 1 and (sys.argv[1] == '-l' or sys.argv[1] == '-local')):
    dev = True
    print('RUNNING IN LOCAL MODE (Non Google App Engine)')

if dev:
    app = bottle
else:
    app = Bottle()

curdir = ''
if dev:
    curdir = os.path.dirname(os.path.abspath(__file__)) + '/'

bottle.TEMPLATE_PATH.insert(0, curdir + 'template/')

# Setup database
conn = sqlite3.connect("database.db")
cur = conn.cursor() 

questions = cur.execute('SELECT * FROM questions').fetchall()

accounts = []

STUDENTS_EDIT_URL = '/admin/students/'
SESSIONID_COOKIE_STRING = 'math-drill_SID'

@app.route('/')
def index():
    students = getStudents()
    student = ('No students - add them in the admin menu!', None)
    if (len(students) > 1):
        student = students[random.randint(0, len(students) - 1)]
    
    question = questions[random.randint(0, len(questions) - 1)]
    
    return bottle.template('drill.tpl',
                           imgpath="/static/img/" + question[1],
                           imgalt="Question",
                           student=student[0],
                           question=question[0])


@app.route('/static/:path#.+#')
def server_static(path):
    return bottle.static_file(path, root=curdir + "/static/")


@app.error(404)
def Error404(code):
    return 'Error 404'


@app.route('/admin/')
def adminIndex():
    username = checkAuth()
    if username:
        return bottle.template('admin.tpl', username=username)
    else:
        return bottle.template('accessdenied.tpl')


@app.route('/admin/login/')
def login():
    if (checkAuth()):
        return '<p>You are already logged in.</p>'
    else:
        return bottle.template('login.tpl')


@app.route('/admin/logout/')
def logout():
    loAccount = 'null'
    for i in range(0,len(accounts)):
        authCookie = request.get_cookie(SESSIONID_COOKIE_STRING, secret=accounts[i][1])
        if authCookie and accounts[i][0] == authCookie:
            loAccount = authCookie
            del accounts[i] 
    return loAccount + ' has been logged out.'

@app.post('/admin/login/submit/')
def postLogin():
    username = request.forms.get('username').lower()
    password = request.forms.get('password')
    print('/login/submit:', accounts)
    sqlCmd = 'SELECT * FROM users WHERE id = ?'
    print(sqlCmd)
    # Execute command, securely replacing '?' with username, contained in a tuple
    filedPassword = cur.execute(sqlCmd, (username, )).fetchone()
    print(filedPassword)
    if (filedPassword == None):
        return '<h2>Invalid username or password</h2>'

    if(checkPassword(password, filedPassword[2], filedPassword[1])):
        temp = False
        # Check if user is already in accounts array, and if so, delete them.
        for i in range(0,len(accounts)):
            if username == accounts[i][0]:
                del accounts[i]
                temp = True
        
        sessionID = createSalt()
        accounts.append(( username, sessionID))
        response.set_cookie(SESSIONID_COOKIE_STRING, username, secret=sessionID, path='/')
        print('Sent cookie:', SESSIONID_COOKIE_STRING + ',',  username + ',', sessionID)
        if temp:
            return 'Deleted old account entry'
        else:
            bottle.redirect('/admin/')
    else:
        return '<h2>Invalid username or password</h2>'


def checkAuth():
    #return "Insecure"
    print (accounts)
    for account in accounts:
        authCookie = request.get_cookie(SESSIONID_COOKIE_STRING, secret=account[1])
        if authCookie and account[0] == authCookie:
            return account[0]
        else:
            return None


def createSalt():
    return uuid.uuid4().hex


def createPassword(password_str, salt):
    return hashlib.sha256((salt + password_str).encode())


def checkPassword(password_str, salt, hashed_pass):
    return hashlib.sha256((salt + password_str).encode()).hexdigest() == hashed_pass


@app.route(STUDENTS_EDIT_URL)
def editStudents():
    username = checkAuth()
    students = cur.execute('SELECT * FROM students').fetchall()
    
    if (not username):
        return '<p>Access denied, please <a href=\"/admin/login/\">sign in</a>.</p>'

    return bottle.template('students.tpl', students=students, username=username)


@app.post(STUDENTS_EDIT_URL + 'submit/')
def postStudents():
    if (not checkAuth()):
        return '<p>Access denied, please <a href=\"/admin/login/\">sign in</a>.</p>'
    # Variable to add output to POST page
    output = ''
    # List for compiling changes, will become a 2 dimensional list
    students = getStudents()     
    for student in students:
        # Check if any of the deletion check boxes were active
        print('Checking against student', student[0])
        if request.forms.get(student[0] + '_delete') == 'del':
            print('Deleting student', student[0])
            cur.execute('DELETE FROM students WHERE studentname=?', (student[0],))

    # Variable to store the user input into the add students textarea
    addStudentsRaw = request.forms.get('add_students')
   
    # Check if there is data in the Add Students textarea
    if addStudentsRaw != None:
        addStudents = addStudentsRaw.split('\n')
        # Add students from textarea to students[] list
        for student in addStudents:
            # Sanitizes inputs by removing all non letters/numbers
            student = re.sub('[\W_]+ ', '', student)
            student = student.strip()
            # Name cannot be null
            if  student != '' and student != None: 
                cur.execute('INSERT INTO students VALUES(?)', (student,))

    print('Applying to database')
    conn.commit()
    cur.close
    bottle.redirect(STUDENTS_EDIT_URL)


def getStudents():
    return cur.execute('SELECT * FROM students').fetchall()

if dev:
    bottle.run(debug=True)
else:
    bottle.run(app=app, server="gae", debug=True) 
