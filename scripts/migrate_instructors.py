from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]

courses = list(db.courses.find())

for c in courses:
    instructor = c.get("instructor")

    if not instructor:
        continue

    # Tạo record giảng viên
    teacher = {
        "name": instructor.get("name"),
        "bio": instructor.get("bio"),
        "avatar": instructor.get("avatar")
    }

    # Thêm giảng viên vào collection teachers
    result = db.teachers.insert_one(teacher)
    teacher_id = str(result.inserted_id)

    # Cập nhật khóa học → thay instructor bằng instructor_id
    db.courses.update_one(
        {"_id": c["_id"]},
        {
            "$set": {"instructor_id": teacher_id},
            "$unset": {"instructor": ""}  
        }
    )

print("DONE - Đã migrate toàn bộ giảng viên")
