#6D/19090062/Gina sonia w
#6D/19090032/Moh izzul fuadi
#6D/19090081/Miftakhul Nizar
#6D/19090128/Annon pri antomo

from datetime import datetime
import os, random, string
from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "user.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True,nullable=False)
    password = db.Column(db.String(20), unique=False,nullable=False)
    token = db.Column(db.String(20), unique=False,nullable=True)
    
class events(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    event_creator = db.Column(db.String(20), unique=False,nullable=False)
    event_name = db.Column(db.String(20), unique=False,nullable=False)
    event_start_time = db.Column(db.DateTime, unique=False,nullable=False)
    event_end_time = db.Column(db.DateTime, unique=False,nullable=False)
    event_start_lat= db.Column(db.String(20), unique=False,nullable=False)
    event_start_lng =db.Column(db.String(20), unique=False,nullable=False)
    event_finish_lat = db.Column(db.String(20), unique=False,nullable=False)
    event_finish_lng = db.Column(db.String(20), unique=False,nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.now)

class logs(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(20), nullable=False)
    event_name = db.Column(db.String(20), nullable=False)
    log_lat = db.Column(db.String(20), nullable=False)
    log_lng = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now)


db.create_all()

@app.route("/api/v1/users/create", methods=["POST"])
def add_users():
  username = request.json['username']
  password = request.json['password']
  
  newUsers = users(username=username, password=password)

  db.session.add(newUsers)
  db.session.commit() 
  return jsonify({
    'msg': 'registrasi sukses'
    
    })

@app.route("/api/v1/users/login", methods=["POST"])
def login():
  username = request.json['username']
  password = request.json['password']

  user = users.query.filter_by(username=username, password=password).first()

  if user:
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    users.query.filter_by(username=username, password=password).update({'token': token})
    db.session.commit()

    return jsonify({
      'msg': 'Login anda berhasil',
      'token': token
      })

  else:
    return jsonify({
      'msg': 'Login anda gagal',
      'status': 401,
      })

@app.route("/api/v1/event/create", methods=["POST"])
def info():
  token = request.json['token']
  token = users.query.filter_by(token=token).first()
  if token:
     event_creator = token.username
     event_name = request.json['event_name']
     event_start_time = request.json['event_start_time']
     event_end_time = request.json['event_end_time']
     event_start_lat= request.json['event_start_lat']
     event_start_lng = request.json['event_start_lng']
     event_finish_lat = request.json['event_finish_lat']
     event_finish_lng = request.json['event_finish_lng']
     event_start_time = datetime.strptime(event_start_time, '%Y-%m-%d %H:%M:%S') 
     event_end_time= datetime.strptime(event_end_time, '%Y-%m-%d %H:%M:%S')

     newevent = events(event_creator= event_creator , event_name = event_name, event_start_time = event_start_time, event_end_time = event_end_time, event_start_lat = event_start_lat, event_start_lng= event_start_lng, event_finish_lat = event_finish_lat, event_finish_lng = event_finish_lng)
     
     
     db.session.add(newevent)
     db.session.commit()
     return jsonify({

        'msg': 'event berhasil ditambahkan!'
        })
  else:
      return jsonify({
        'msg': 'token salah'
        })

@app.route("/api/v1/events/log", methods=["POST"])
def events_log():
    token = request.json['token']
    token = users.query.filter_by(token=token).first()
    if token:
       
      username = token.username
      event_name = request.json['event_name']
      log_lat = request.json['log_lat']
      log_lng = request.json['log_lng']
   
      newLog = logs(username=username, event_name=event_name, log_lat=log_lat, log_lng=log_lng)

      db.session.add(newLog)
      db.session.commit() 
      return jsonify({'msg': 'sukses mencatat posisi baru'})
    else:
        return jsonify({'msg': 'token salah'})

@app.route("/api/v1/events/logs", methods=["GET"])
def event_logs():
    token = request.json['token']
    token = users.query.filter_by(token=token).first()
    if token:

     username = token.username
     event_name = request.json['event_name']
     
     logss= logs.query.filter_by(event_name=event_name).all()
    
    array_Log = []
    for log in logss:
        dict_books = {}
        dict_books.update({"username": log.username,"event_name": log.event_name,"log_lat": log.log_lat, "log_lng": log.log_lng })
        array_Log.append(dict_books)
    return jsonify(array_Log)

if __name__ == '__main__':
   app.run(debug = True, port=7092)
