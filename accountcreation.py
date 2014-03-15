import uuid
import hashlib
import getpass
import sqlite3
import run

conn = sqlite3.connect("database.db")
cur = conn.cursor() 

def createAccount(username, password, salt):
    cur.execute('INSERT INTO users VALUES(?,?,?)', (username, password.hexdigest(), salt))
    conn.commit()
    cur.close
    print('Entered into database.')


def createMode():
    username = input('Enter username: ')
    salt = run.createSalt()
    pass1 = run.createPassword(getpass.getpass('Enter password: '), salt)
    pass2 = run.createPassword(getpass.getpass('Enter password again: '), salt)

    if (pass1.hexdigest() == pass2.hexdigest()):
        createAccount(username, pass1, salt)
    else:
        print('Passwords did not match')

def clear1Mode():
    username = input('Enter username to clear: ')
    cur.execute('DELETE FROM users WHERE id = ?', (username,))
    conn.commit()
    cur.close

def clearAllMode():
    confirm = input('Are you sure you want to clear all users? (yes/no)')
    if confirm == 'yes' or confirm == 'y':
        cur.execute('DELETE FROM users')
        conn.commit()
        cur.close
    else:
        print('Did not delete.')

def listMode():
    for tup in cur.execute('SELECT * FROM users').fetchall():
        print(tup)

mode = input('0 - Add Account\n1 - Clear Specific Account\n2 - Clear All Accounts\n3 - List All Accounts: ')
if mode == '0':
    createMode()
elif mode == '1':
    clear1Mode()
elif mode == '2':
    clearAllMode()
elif mode == '3':
    listMode()
else:
    print('Invalid choice', mode)
