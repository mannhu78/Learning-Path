from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]

teachers_col = db["teachers"]
courses_col = db["courses"]

teachers_col.delete_many({})  # XÓA HẾT GIẢNG VIÊN CŨ

unique_teachers = {}

for c in courses_col.find():
    inst = c.get("instructor")
    if inst:
        key = inst["name"]

        if key not in unique_teachers:
            teacher_id = teachers_col.insert_one(inst).inserted_id
            unique_teachers[key] = teacher_id
        else:
            teacher_id = unique_teachers[key]

        courses_col.update_one(
            {"_id": c["_id"]},
            {
                "$set": {"instructor_id": teacher_id},
                "$unset": {"instructor": ""}  # xoá instructor cũ trong course
            }
        )

print("✔ DONE! Đã migrate instructors vào collection teachers.")
