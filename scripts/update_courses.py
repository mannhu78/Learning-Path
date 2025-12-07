from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
courses = db["courses"]

# Lý thuyết mặc định
default_theory = "Nội dung lý thuyết đang được cập nhật."

# Tài liệu mặc định
default_resources = [
    "https://www.w3schools.com",
    "https://www.geeksforgeeks.org"
]

# Update tất cả khóa học chưa có trường theory/resources
result = courses.update_many(
    {},
    {
        "$set": {
            "theory": default_theory,
            "resources": default_resources
        }
    }
)

print("Updated:", result.modified_count, "courses")
