from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
users = db["users"]

default_fields = {
    "avatar": "/static/img/users/default.png",
    "about": "",
    "saved_courses": [],
    "completed_courses": [],
    "learning_paths": [],
    "created_at": datetime.datetime.utcnow(),
    "updated_at": datetime.datetime.utcnow()
}

updated = 0

for user in users.find():
    update_fields = {}

    for key, value in default_fields.items():
        if key not in user:
            update_fields[key] = value

    if update_fields:
        users.update_one({"_id": user["_id"]}, {"$set": update_fields})
        updated += 1

print(f"Đã cập nhật: {updated} user.")
