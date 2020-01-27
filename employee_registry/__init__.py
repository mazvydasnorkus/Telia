import markdown   # converting string to HTML
import os         # manipulating file paths
import shelve     # to get values from db not keys

# Import the framework
from flask import Flask, g  # Flask - Flask framework, g - to manage resources during a request
from flask_restful import Resource, Api, reqparse  


app = Flask(__name__)
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("employees.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class EmployeeList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        employees = []

        for key in keys:
            employees.append(shelf[key])

        return {'message': 'Success', 'data': employees}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('birth_date', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['name']] = args

        return {'message': 'Employee registered', 'data': args}, 201


class Employee(Resource):
    def get(self, name):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (name in shelf):
            return {'message': 'Employee not found', 'data': {}}, 404

        return {'message': ' found', 'data': shelf[name]}, 200

    def delete(self, name):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (name in shelf):
            return {'message': 'Employee not found', 'data': {}}, 404

        del shelf[name]
        return '', 204


api.add_resource(EmployeeList, '/employees')
api.add_resource(Employee, '/employee/<string:name>')
