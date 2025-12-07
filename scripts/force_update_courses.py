from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
courses = db["courses"]

# Mapping THEORY theo category
category_theory_map = {
    "Web Development": "Nội dung Web Development...",
    "Backend Development": "Nội dung Backend...",
    "Programming": "Nội dung Programming...",
    "Database": "Nội dung Database...",
    "Mobile Development": "Nội dung Mobile...",
    "DevOps": "Nội dung DevOps...",
    "Cloud": "Nội dung Cloud...",
    "Data Science": "Nội dung Data Science...",
    "AI & ML": "Nội dung AI & ML...",
    "Cybersecurity": "Nội dung Cybersecurity...",
    "QA / Testing": "Nội dung QC và Testing...",
    "Tools": "Nội dung Tools...",
    "Software Engineering": "Nội dung SE..."
}

# Mapping RESOURCES theo category
category_resources_map = {
    "Web Development": ["https://developer.mozilla.org", "https://w3schools.com"],
    "Backend Development": ["https://postman.com", "https://swagger.io"],
    "Programming": ["https://geeksforgeeks.org"],
    "Database": ["https://mongodb.com/docs"],
    "Mobile Development": ["https://developer.android.com"],
    "DevOps": ["https://docs.docker.com"],
    "Cloud": ["https://aws.amazon.com"],
    "Data Science": ["https://pandas.pydata.org/docs"],
    "AI & ML": ["https://scikit-learn.org"],
    "Cybersecurity": ["https://owasp.org"],
    "QA / Testing": ["https://softwaretestinghelp.com"],
    "Tools": ["https://git-scm.com/doc"],
    "Software Engineering": ["https://martinfowler.com"]
}

updated = 0

for course in courses.find():
    cat = course.get("category")

    new_theory = category_theory_map.get(cat, "Nội dung đang được cập nhật.")
    new_resources = category_resources_map.get(cat, ["https://google.com"])

    courses.update_one(
        {"_id": course["_id"]},
        {"$set": {
            "theory": new_theory,
            "resources": new_resources
        }}
    )
    
    updated += 1

print("Đã cập nhật:", updated, "khóa học.")
