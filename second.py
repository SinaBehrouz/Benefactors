"""
    Description: sets up flask app with multiple method types + path parameters 
    just getting a bit fancier with it 
"""
# TO DO : Take out demo comments

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# again, highlight the simplicity of decorater 
# methods = the methods allowed for the function
@app.route('/student/<int:student_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def student_info(student_id):
    if request.method == 'GET':
        # could replace this with function call to get student info from db 
        student_info = {
            'studentId': student_id,
            'firstName': "John",
            'lastName': "Ham",
            'major': "Computing Science"
        }
        # jsonify info with status code 
        return jsonify({"info retrieved": student_info}), 200
    elif request.method == 'POST': 
        # could replace this with function call to create student in db 
        student_info = request.get_json()
        return jsonify({'student recorded': student_info}), 201
    elif request.method == 'PUT':
         # could replace this with function call to update student in db
        updated_student_info = request.get_json()
        return jsonify({'student info updated': updated_student_info}), 200
    elif request.method == 'DELETE':
        # could replace this with function call to delete student in db
        return jsonify({'student deleted': student_id}), 200

if __name__ == '__main__':
    app.run(debug=True)