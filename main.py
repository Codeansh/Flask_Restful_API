
from email import message
import re
from flask import Flask  #, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, marshal_with, fields

app = Flask(__name__)

api = Api(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Videodb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    views = db.Column(db.Integer,nullable=False)
    likes = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f"name: {name}, id :{id}, views: {views}, likes: {likes}"
# database needs to be crearted only once otherwise database will be  overwritten
#db.create_all()


video_req_parser = reqparse.RequestParser()

video_req_parser.add_argument("name", type=str, help="Name is required", required = True)
video_req_parser.add_argument("views", type=int, help="Views field is required", required = True)
video_req_parser.add_argument("likes", type=int, help="Likes field is required", required = True)

video_update_parser = reqparse.RequestParser()

video_update_parser.add_argument("name", type=str, help="Name is required")
video_update_parser.add_argument("views", type=int, help="Views field is required" )
video_update_parser.add_argument("likes", type=int, help="Likes field is required")

videos = {}

# def abort_when_no_id(video_id):
#     if not video_id in videos:
#         abort(404, message='video not found')

# def abort_when_same_id(video_id):
#     if  video_id in videos:
#         abort(409, message='video_id aready exists')       
resource_fields = {
  'id' : fields.Integer,
  'name' : fields.String,
  'views' : fields.Integer,
  'likes' : fields.Integer

}
class Video(Resource):


    @marshal_with(resource_fields)
    def get(self,video_id):
        result = Videodb.query.filter_by(id=video_id).first()

        #abort_when_no_id(video_id)
        #return {video_id :videos[video_id]}
        if not result:
            abort(404,message="Couldn't find video with that id")
        return result
    # def post(self,video_id)
    #     return {"data" : "Posted"}

    @marshal_with(resource_fields)
    def put(self,video_id):
        # abort_when_same_id(video_id)
        args = video_req_parser.parse_args()
        result = Videodb.query.filter_by(id=video_id).first()
        if result :
            abort(409, message="video-id already taken")
        video = Videodb(id=video_id,name=args['name'], views=args['views'],likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        # videos[video_id] = args
        # return videos[video_id], 201
        return video


        # data = request.form
        # print(data)
    # def delete(self,video_id):
    #     abort_when_no_id(video_id)
    #     del videos[video_id]
    #     return ' ',204
    @marshal_with(resource_fields)    
    def patch(self, video_id):
        result = Videodb.query.filter_by(id=video_id).first()
        if not result :
            abort(404,message="Couldn't find video with that id")
        args = video_update_parser.parse_args()

        if args["name"]:
            result.name = args["name"]
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        db.session.commit()
        return result    


api.add_resource(Video,"/video/<int:video_id>")



if __name__ == "__main__":
    app.run(debug=True)