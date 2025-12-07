from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]

cats = db.courses.distinct("category")

print("CÁC CATEGORY ĐANG CÓ TRONG DATABASE:")
for c in cats:
    print(f"- '{c}'")
