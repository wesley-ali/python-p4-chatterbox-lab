from email import message
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Your routes and other configurations...


from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db, )

db.init_app(app)

@app.route('/messages',methods = ["GET","POST"])
def messages():
     if request.method == "GET":
        messages = Message.query.order_by(Message.created_at).all()
        messages_dict = [message.to_dict() for message in messages]
        response = make_response(messages_dict,200,{"Content-Type":"application/json"})
        return response
     elif request.method == "POST":
        data = request.get_json()
        message = Message(
            body=data["body"],
            username=data['username']
        )


     db.session.add(message)
     db.session.commit()

     return  make_response(message.to_dict(),  201,)

@app.route('/messages/<int:id>',methods = ["PATCH","DELETE"])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == "DELETE":
        db.session.delete(message)
        db.session.commit()
        response_body = {"message" : "Deletion successful"}
        return make_response(response_body,200)
    
    elif request.method == "PATCH":
        for attr in request.get_json():
            setattr(message,attr,request.get_json()[attr])
        db.session.add(message)
        db.session.commit()
        response = make_response(message.to_dict(),200)
        return response

if __name__ == '__main__':
    app.run(port=5555)
