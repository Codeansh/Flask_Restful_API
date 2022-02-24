from flask import Flask  #, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)

api = Api(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Video(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    views = db.Column(db.Integer,nullable=False)
    likes = db.Column(db.Integer,nullable=False)
db.create_all()


video_req_parser = reqparse.RequestParser()

video_req_parser.add_argument("name", type=str, help="Name is required", required = True)
video_req_parser.add_argument("views", type=int, help="Views field is required", required = True)
video_req_parser.add_argument("likes", type=int, help="Likes field is required", required = True)
videos = {}

def abort_when_no_id(video_id):
    if not video_id in videos:
        abort(404, message='video not found')

def abort_when_same_id(video_id):
    if  video_id in videos:
        abort(409, message='video_id aready exists')       

class Video(Resource):
    def get(self,video_id):
        abort_when_no_id(video_id)
        return {video_id :videos[video_id]}

    # def post(self,video_id)
    #     return {"data" : "Posted"}

    def put(self,video_id):
        abort_when_same_id(video_id)
        args = video_req_parser.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

        # data = request.form
        # print(data)
    def delete(self,video_id):
        abort_when_no_id(video_id)
        del videos[video_id]
        return ' ',204
        


api.add_resource(Video,"/video/<int:video_id>")



if __name__ == "__main__":
    app.run(debug=True)