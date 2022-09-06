import psycopg2
import random
from random import choice
import string
from settings import user, password, host, database


"""
Script for creating three databases for students, groups, courses 
and filling it with data according to task requirements.
"""

try:
    # connect to exist database. For connection please use your parameters from environment.
    connection = psycopg2.connect(host, user, password, database)
    connection.autocommit = True

    # create a new tables: groups, students and courses
    # for groups
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE groups(
                id SERIAL PRIMARY KEY,
                name varchar(7) NOT NULL);"""
        )
        print("[INFO] Table groups created successfully 1/4")

    # for students
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE students(
                id SERIAL PRIMARY KEY,
                group_id varchar(7),
                first_name varchar(30) NOT NULL,
                last_name varchar(30) NOT NULL);"""
        )
        print("[INFO] Table students created successfully 2/4")

    # for courses
    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE courses(
                id SERIAL PRIMARY KEY,
                name varchar(30) NOT NULL,
                description varchar(400));"""
        )
        print("[INFO] Table courses created successfully 3/4")

    with connection.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE assoc_table(
                id SERIAL PRIMARY KEY,
                student_id integer,
                course_id integer);"""
        )
        print("[INFO] Table assoc_table created successfully 4/4")

    # insert data into a groups table. for generating the names of groups create the list dump_for_groups
    dump_for_groups = []
    for _ in range(10):
        dump_for_groups.append(
            choice(string.ascii_uppercase) + choice(string.ascii_uppercase) + '-' + choice(string.digits) + choice(
                string.digits))

    # insert = dump_for_groups
    for i in range(10):
        insert = dump_for_groups[i]
        sql = "INSERT INTO groups (name) VALUES (%s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (insert,))
    print("[INFO] Data for table groups were successfully inserted 1/4")

    # insert data into a courses table
    with connection.cursor() as cursor:
        cursor.execute(
            """INSERT INTO courses (name, description) VALUES
            ('Math', 'Mathematics is the science and study of quality, structure, space, and change.'),
            ('Biology', 'Biology is the study of life. The word "biology" is derived from the Greek words "bios" (meaning life) and "logos" (meaning "study").'),
            ('Geometry', 'Geometry is a branch of mathematics that studies the sizes, shapes, positions, angles, and dimensions of things. 2D Shapes in Geometry.'),
            ('Chemistry', 'Chemistry is the scientific study of the properties and behavior of matter. It is a natural science that covers the elements that make up matter to the compounds composed of atoms, molecules and ions: their composition, structure, properties, behavior and the changes they undergo during a reaction with other substances.'),
            ('Physics', 'Physics is the branch of science that deals with the structure of matter and how the fundamental constituents of the universe interact. It studies objects ranging from the very small using quantum mechanics to the entire universe using general relativity.'),
            ('Geography', 'Geography is a field of science devoted to the study of the lands, features, inhabitants, and phenomena of the Earth and planets. '),
            ('Economics', 'Economics is the study of scarcity and its implications for the use of resources, production of goods and services, growth of production and welfare over time, and a great variety of other complex issues of vital concern to society.'),
            ('Architecture', 'Architecture is defined as the art and science of designing buildings and structures. A wider definition would include within this scope the design of any built environment, structure or object, from town planning, urban design, and landscape architecture to furniture and objects.'),
            ('Programming', 'Computer programming is the process of performing a particular computation (or more generally, accomplishing a specific computing result), usually by designing and building an executable computer program. Programming involves tasks such as analysis, generating algorithms, profiling algorithms accuracy and resource consumption, and the implementation of algorithms.'),
            ('History', 'History is the study and the documentation of the past. Events before the invention of writing systems are considered prehistory. "History" is an umbrella term comprising past events as well as the memory, discovery, collection, organization, presentation, and interpretation of these events.');"""
        )
        print("[INFO] Data for table courses were successfully inserted 2/4")

    # insert data into students table
    first_names = ['Oliver', 'Jack', 'Harry', 'Jacob', 'Jake', 'Thomas', 'James', 'Oscar', 'William', 'David'
                                                                                                      'Amelia',
                   'Olivia', 'Isla', 'Sophia', 'Sarah', 'Tracy', 'Ava', 'Isabella', 'Lily', 'Joanne']
    last_names = ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'White', 'Harris', 'Martin', 'Davies', 'Wilson',
                  'Cooper', 'Evans', 'King', 'Thomas', 'Baker', 'Green', 'Clark', 'Wright', 'Johnson', 'Robinson']

    for i in range(200):
        insert_group = choice(dump_for_groups)
        insert_first = choice(first_names)
        insert_last = choice(last_names)
        sql = "INSERT INTO students (group_id, first_name, last_name) VALUES (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(sql, (insert_group, insert_first, insert_last,))
    print("[INFO] Data for table students were successfully inserted 3/4")

    # create a list for students as 3 parts because we need assign for them up to 3 courses. So this list will include
    # some students in 1 time some in 2 and some in 3
    list_for_courses, list_for_students, lfs_1, lfs_2, lfs_3 = [], [], [], [], []
    [lfs_1.append(x) for x in range(1, 69)]

    [lfs_2.append(x) for x in range(69, 133)]
    [lfs_2.append(x) for x in range(69, 133)]
    lfs_2.sort()

    [lfs_3.append(x) for x in range(133, 201)]
    [lfs_3.append(x) for x in range(133, 201)]
    [lfs_3.append(x) for x in range(133, 201)]
    lfs_3.sort()

    list_for_students = lfs_1 + lfs_2 + lfs_3

    # create list for courses by append random 1-10 element with avoiding near duplicates
    list_for_courses = [random.randint(1, 10)]
    for index in range(1, 400):
        temp_value = random.randint(1, 10)
        while temp_value == list_for_courses[index - 1] or temp_value == list_for_courses[index - 2]:
            temp_value = random.randint(1, 10)
        list_for_courses.append(temp_value)

    sql = "INSERT INTO assoc_table (student_id, course_id) VALUES (%s, %s)"
    for i in range(400):
        with connection.cursor() as cursor:
            cursor.execute(sql, (list_for_students[i], list_for_courses[i]))

    print("[INFO] Data for table assoc_table were successfully inserted 4/4")

except Exception as _ex:
    print("[INFO] Error while working with PostgresSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")
