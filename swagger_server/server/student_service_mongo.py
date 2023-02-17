import json
import os
import tempfile
from functools import reduce

from tinydb import TinyDB, Query
# MongoDB
from pymongo import MongoClient
from bson.objectid import ObjectId


db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)

# MongoDB setup
# Connect to local mongoDB
connectionStr = "mongodb://localhost:27017/"
client = MongoClient(connectionStr)
db = client["studentService"]
col = db["student"]



def add(student=None):

    r = col.find_one({"first_name":student.first_name, "last_name":student.last_name})
    if r is not None:
        return 'already exists', 409

    total = col.count_documents({}) + 1
    newStudent = {"student_id": total, "first_name": student.first_name, "last_name": student.last_name}
    r = col.insert_one(newStudent)

    return total


def get_by_id(student_id=None, subject=None):
    r = col.find_one({'student_id': student_id})
    if r is None:
        return 'not found', 404
    print(str(r))
    return str(r)




def delete(student_id=None):
    r = col.find_one({'student_id':student_id})
    if r is None:
        return 'not found', 404
    col.delete_one({'student_id':student_id})
    return student_id
