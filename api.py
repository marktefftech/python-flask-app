from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

STUDENTS = {
    '1': {'name': 'Mark', 'age': 22, 'spec': 'Math'},
    '2': {'name': 'Jane', 'age': 20, 'spec': 'History'},
    '3': {'name': 'George', 'age': 28, 'spec': 'Science'},
    '4': {'name': 'Alfred', 'age': 29, 'spec': 'Geo'}
}

parser = reqparse.RequestParser()

class StudentsList(Resource):
    def get(self):
        return STUDENTS

    def post(self):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        student_id = int(max(STUDENTS.keys())) + 1
        student_id = '%i' % student_id
        STUDENTS[student_id] = {
            "name": args["name"],
            "age": args["age"],
            "spec": args["spec"]
        }
        return STUDENTS[student_id], 201

# Perform operations on a single student 
class Student(Resource):
    # Get single student if exist
    def get(self, student_id):
        if student_id not in STUDENTS:
            return "Not Found", 404
        else:
            return STUDENTS[student_id]

    # Update a single student if exist
    def put(self, student_id):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        if student_id not in STUDENTS:
            return "Record Not Found", 404
        else:
            student = STUDENTS[student_id]
            student["name"] = args["name"] if args["name"] is not None else student["name"]
            student["age"] = args["age"] if args["age"] is not None else student["age"]
            student["spec"] = args["spec"] if args["spec"] is not None else student["spec"]
            return student, 200

    def delete(self, student_id): 
        if student_id not in STUDENTS:
            return "Not Found", 404
        else:
            del STUDENTS[student_id]
            return '', 204



api.add_resource(StudentsList, '/students/')
api.add_resource(Student, '/students/<student_id>')

if __name__ ==  '__main__':
    app.run(debug=True)