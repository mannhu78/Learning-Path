from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
teachers = db["teachers"]

# Mapping giáo viên -> lĩnh vực
category_map = {
    "Nguyễn Minh H": "Web Development",
    "Nguyễn Vũ M": "Programming",
    "Trần Quốc B": "Backend Development",
    "Võ Đức T": "Database",
    "Hồ Văn D": "Mobile Development",
    "Nguyễn Hoàng K": "DevOps",
    "Huỳnh Ngọc S": "Cloud",
    "Lê Minh Q": "Data Science",
    "Phạm Tuấn A": "AI & ML",
    "Dương Tấn P": "Cybersecurity",
    "Phạm Tuyết L": "QA / Testing",
    "Hạnh B": "Tools",
    "Đào Bảo L": "Software Engineering"
}

updated = 0

for t in teachers.find():
    name = t["name"]

    if name in category_map:
        db.teachers.update_one(
            {"_id": t["_id"]},
            {"$set": {"category": category_map[name]}}
        )
        updated += 1

print(f"✔ Đã cập nhật category cho {updated} giáo viên!")
