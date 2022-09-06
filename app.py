from flask import request, jsonify, render_template
from sqlalchemy import func
from models import *


# Init app
app = Flask(__name__)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)


# HOME page
"""THE SIMPLE HOME PAGE FOR OUR PROJECT WITH ALL OPTIONS WHICH CAN TO DO"""


@app.route('/')
def index():
    tittle = 'HOME'
    content = "Hello! You are on the Home page of Students and Courses web-magazine ^_^"
    return render_template("index.html", tittle=tittle, content=content)


# Get All Students
"""TO SEE ALL STUDENTS IN OUR PROJECT"""


@app.route('/students', methods=['GET'])
def get_students():
    all_students = Students.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)


"""FIND ALL GROUPS WITH LESS OR EQUAL STUDENTS COUNT."""


@app.route('/all_groups_less_stud')
def count_min_group_by_students():
    gr_st_list = Students.query.with_entities(Students.group_id, func.count(Students.group_id)).group_by(Students.group_id).all()
    gr_st_list.sort(key=lambda x: x[1])
    result = []
    [result.append(ele[0]) for ele in gr_st_list if ele[1] == gr_st_list[0][1]]
    return f'The minimal q-ty of students is {gr_st_list[0][1]} in group(s): {result}'

"""END OF THIS TASK"""

"""FIND ALL STUDENTS RELATED TO THE COURSE WITH A GIVEN NAME."""


@app.route('/course_name_to_find_students_form', methods=['GET'])
def course_name_to_find_student():
    return render_template("course_name_to_find_students_form.html")


@app.route('/all_students_on_course', methods=['POST'])
def find_all_students_on_course():
    course_name = request.form["name"]
    needed_course = Courses.query.filter_by(name=course_name).first()
    course_id = needed_course.id
    list_of_all_assoc = AssocTable.query.filter_by(course_id=course_id).all()
    list_stud_id = []
    [list_stud_id.append(ele.student_id) for ele in list_of_all_assoc]
    all_students = Students.query.filter(Students.id.in_(list_stud_id)).all()
    result = students_schema.dump(all_students)
    return jsonify(result)


"""END OF THIS TASK"""

"""CREATE NEW STUDENT"""


@app.route('/add_new_student_form/', methods=['GET'])
def collect_data_for_new_student():
    return render_template("add_new_student_form.html")


@app.route('/add_new_student', methods=['POST'])
def add_new_student():
    group_id = request.form["group_id"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    try:
        new_student = Students(group_id, first_name, last_name)
        db.session.add(new_student)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("The mistake in adding new student")
    return student_schema.jsonify(new_student)


"""END OF THIS TASK"""

"""DELETE STUDENT BY STUDENT_ID"""


@app.route('/delete_student_form', methods=['GET'])
def collect_data_for_delete_student():
    return render_template("delete_student_form.html")


@app.route('/delete_student', methods=['POST'])
def delete_student():
    stud_id = request.form["stud_id"]
    try:
        student = Students.query.filter_by(id=stud_id).first()
        db.session.delete(student)
        db.session.commit()
    except:
        db.session.rollback()
        print("The mistake in deleting student, please check students ID")
    return student_schema.jsonify(student)


"""END OF THIS TASK"""

"""ADD A STUDENT TO THE COURSE (from a list)"""


@app.route('/add_student_to_course_form', methods=['GET'])
def collect_data_for_adding_student_to_course():
    return render_template("add_student_to_course_form.html")


@app.route('/add_student_to_course', methods=['POST'])
def add_student_to_course():
    stud_id = request.form["stud_id"]
    course_id = request.form["course_id"]
    try:
        ac = AssocTable(student_id=stud_id, course_id=course_id)
        db.session.add(ac)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        print("The mistake in adding student on course. Please check the IDs")
    student = Students.query.filter_by(id=stud_id).first()
    return student_schema.jsonify(student)


"""END OF THIS TASK"""

"""REMOVE THE STUDENT FROM ONE OF HIS OR HER COURSES."""


@app.route('/remove_stud_from_course_form', methods=['GET'])
def collect_data_for_student_and_course():
    return render_template("remove_student_from_course_form.html")


@app.route('/remove_stud_from_course', methods=['POST'])
def remove_student_from_course():
    stud_id = request.form["stud_id"]
    course_id = request.form["course_id"]
    try:
        for_del = AssocTable.query.filter_by(student_id=stud_id, course_id=course_id).first()
        db.session.delete(for_del)
        db.session.commit()
    except:
        db.session.rollback()
        return "The mistake in deleting course from student, please check IDs"
    return "The student successfully removed from course"


"""END OF TASK"""

# Run server
if __name__ == '__main__':
    app.run(debug=True)
