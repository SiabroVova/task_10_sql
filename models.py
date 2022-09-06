from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from settings import user, password, host, database

# Init app
app = Flask(__name__)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Associate table for many-to-many relationship between students and courses
class AssocTable(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)


# Students Class/Model
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    def __init__(self, group_id, first_name, last_name):
        self.group_id = group_id
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return f'<Student: {self.first_name} {self.last_name} from group: {self.group_id}.>'


# Students Schema
class StudentSchema(ma.Schema):
    id = fields.Str()
    group_id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


# Init schema
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)


# Courses Class
class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(400))

    def __repr__(self):
        return f'<Course - {self.name} has next description - {self.description}>\n'


# Class for Groups
class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'<Group: {self.name}>'
