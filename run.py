from bottle import route, run, template, static_file
import os, bottle, random

curdir =  os.path.dirname(os.path.abspath(__file__))
bottle.TEMPLATE_PATH.insert(0, curdir + '/template/')

students = [line.strip() for line in open('students.txt')]
 
print(">>>>>>>>>>>>>>" + curdir)

@route('/')
def index():
    return server_static('index.html')

@route('/test')
@route('/test/<title>')
def index(title='Test'):
    random_image()
    return server_static("index.html")

@route('/drill')
def generate_question():
    return template('drill.tpl', imgpath="/static/img/" + random_image(), imgalt="Question", question=random_student() + ", what is your opinion on airplane wings?")

def random_student():
    rand = random.randrange(len(students))
    return students[rand]
    

def random_image():
    filelist = os.listdir(curdir + "/static/img/") 
    numimg = 0
    for f in filelist:
        if f.endswith(".png") or f.endswith(".jpg"): 
            print("Found image " + f)
            numimg+= 1
            continue
        else:
            continue
        
    print("Total number of images in dir " + str(numimg))
    rand = random.randrange(numimg)
 
    iterimg = 0 
    for f in filelist:
        if f.endswith(".png") or f.endswith(".jpg"): 
            print("Found image " + f)
            if rand == iterimg:
                return f
            iterimg+= 1
            continue
        else:
            continue
 

#Can use slashes!  I don't know what this does but it works ;)
@route('/static/:path#.+#')
def server_static(path):
    print("LOADING IMAGE FROM: " + curdir + "/static/" + path)
    return static_file(path, root=curdir + "/static/")

run(host='localhost', port=8080)
