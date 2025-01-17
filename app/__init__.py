import datetime
import os
from flask import Flask, render_template, request, json,redirect
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv('./example.env')
app = Flask(__name__)


if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
                    host=os.getenv("MYSQL_HOST"),
                    port=3306)


print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    education_data =[
        {"school": "Western University",
         "year": "2021-2025",
         "img": "./static/img/western.jpg"
        },
        {"school": "Ivey Business School",
         "year": "2023-2025",
         "img": "./static/img/ivey.png"
         },
        {"school": "University of California, Irvine",
         "year": "2021-24",
          "img": "./static/img/uci_logo.png"
        }
    ]

    experience_data = [
        {"company":"Vibemap",
            "title" : "Development Intern",
            "logo":"./static/img/experienceImages/vibemap.jpeg",            
            "date":"May 14, 2023 - Present",
            "description":"Worked as a development intern for the vibemap startup. Learned skills in React, React Native, and Wordpress."},
        
        {"company":"MLH Fellowship",
            "title" : "Site Reliability Engineering Fellow",
            "logo":"./static/img/experienceImages/mlh.png",
            "date": "June 04, 2021 - Present",
            "description":"Worked as a fellow for the MLH Fellowship. Learned skills in React, Flask, and Python."},
        
        {"company":"Western University",
            "title" : "Programming Peer tutor",
            "logo":"./static/img/western.jpg",
            "date":"September 2021 - Present",
            "description":"Worked as a programming peer tutor at Western University. Learned skills in Java, Python, and C++."},

    ]
    return render_template('index.html',title="MLH Fellow", titleEdu="Education", education_data=education_data, titleExp="Experience" ,  experience=experience_data, url=os.getenv("URL"))


@app.route('/hobbies')
def get_hobbies_page():
    # load json data with hobbies, then pass it to the template
    filename = os.path.join(app.static_folder, 'data', 'data.json')
    data = json.load(open(filename))    

    return render_template('hobbies.html', title="Hobbies", url=os.getenv("URL"), data=data['hobbies'])


@app.route('/travels')
def get_travels_page():
    return render_template('travels.html', title="Travels", url=os.getenv("URL"))


@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name,email=email,content=content)

    return model_to_dict(timeline_post)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():

    data = TimelinePost.select().order_by(TimelinePost.created_on.desc())
    data = [model_to_dict(d) for d in data]
    print(datetime.datetime.now())

    return json.dumps(
        data,
        sort_keys=True,
        indent=1,
        default=default )

@app.route('/timeline')
def timeline():
    data = TimelinePost.select().order_by(TimelinePost.created_on.desc())

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        content = request.form.get("content")
        timeline_post = TimelinePost.create(name=name,email=email,content=content)
    redirect('timeline.html')

    print(datetime.datetime.now())

    return render_template('timeline.html', title="timeline", data=data)