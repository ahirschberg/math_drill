import uuid
import hashlib
import getpass
import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor() 

def createAccount(username, password, salt, dbInsert):
    commandInsecure = 'INSERT INTO users VALUES(%s, %s, %s)' % (username, password.hexdigest(), salt)
    if (dbInsert.lower() == 'yes' or dbInsert.lower() == 'y'):
        cur.execute('INSERT INTO users VALUES(?,?,?)', (username, password.hexdigest(), salt))
        conn.commit()
        cur.close
        print('Entered into database.')
    else:
        print('Did not enter into database.\nSQL command is', commandInsecure)


def createSalt():
    return uuid.uuid4().hex


def createPassword(password_str, salt):
    return hashlib.sha256((salt + password_str).encode())


def checkPassword(password_str, salt, hashed_pass):
    return hashlib.sha256((salt + password_str).encode()).hexdigest() == hashed_pass


username = input('Enter username:')
salt = createSalt()
pass1 = createPassword(getpass.getpass('Enter password: '), salt)
pass2 = createPassword(getpass.getpass('Enter password again: '), salt)

if (pass1.hexdigest() == pass2.hexdigest()):
    choice = input('Insert into database? (yes/no) ')
    createAccount(username, pass1, salt, choice)
else:
    print('Passwords did not match')
