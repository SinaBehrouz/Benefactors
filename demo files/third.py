"""
    Description: using flask restful with resourceful routing + showing other things that flask offers  
    Explain why flask restful is so good (e.g explain and show examples of embedded good practiced +  benefits of resourceful routing)
        - resouce deals with routing, helps with seperation of concerns 
        - makes it more elegant e.g with one line routing multiple methods 
        - e.g seperation of concerns 
        - something about good practices ... need to look into this more. 
"""
from flask import Flask, request
from flask_restful import Resource, Api

# TO DO : Take out demo comments
app = Flask(__name__)
# double check exactly how this works so we can explain it conceptually? 
api = Api(app) 

# class inheriting from resource class 
class HelloWorld(Resource):
    def get(self):
        return 'Hello, World!'

# notice no decorater needed, including no need to specify methods in list
# easy to see what type of method 
# different methods go to different pieces of logic + elegant + good seperation of concern here as well 
# no need to clutter your function for checks of method types
# notice/explain resource as arg 

class StudentInfo(Resource): 
    def get(self, student_id):
        # could replace with function to create student in db 
        student_info = {
            'studentId': student_id,
            'firstName': "John",
            'lastName': "Wu",
            'major': "Computing Science"
        }
        return {"Info retrieved ": student_info }, 200
    def post(self, student_id):
        # could replace this with function to create student in db 
        student_info = request.get_json()
        return {'Info recorded ': student_info}, 201 # notice no jsonify, return types are... 
    def put(self, student_id):
        # could replace this with function call to update student in db 
        updated_student_info = request.get_json()
        return {'Info updated ': updated_student_info}, 200
    def delete(self, student_id):
        # could replace this with function call to delete a student in db here   
        to_delete = request.get_json()
        return {'Student deleted ': student_id}, 200


# could even put this in a seperate file, e.g routes.py for even more seperation of concerns
# adding resources to APIs, mapping between endpoint and class name (goes to correct method within class based on type of request)
api.add_resource(HelloWorld, '/')
# notice we only need 1 line for student info, even though we have 4 types of methods (get, post, put, delete)
api.add_resource(StudentInfo, '/student/<int:student_id>') # [GET, POST, PUT, DELETE]


if __name__ == '__main__':
    app.run(debug=True)