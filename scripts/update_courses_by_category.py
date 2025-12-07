from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
courses = db["courses"]

# MAPPING CATEGORY → THEORY
category_theory_map = {
    "Web Development": """
Khóa học Web Development cung cấp kiến thức nền tảng về HTML, CSS, JavaScript,
responsive design, DOM, UI/UX cơ bản và cách xây dựng website hiện đại.
""",

    "Backend Development": """
Khóa học Backend Development tập trung vào API, server-side logic, database integration,
authentication, routing và kiến trúc backend theo chuẩn REST.
""",

    "Programming": """
Khóa học Programming giúp người học hiểu biến, hàm, cấu trúc điều khiển, vòng lặp,
thuật toán cơ bản và lập trình hướng đối tượng – nền tảng của tất cả lĩnh vực CNTT.
""",

    "Database": """
Khóa học Database cung cấp kiến thức về SQL, NoSQL, thiết kế mô hình dữ liệu,
indexing, tối ưu truy vấn và chuẩn hóa cơ sở dữ liệu.
""",

    "Mobile Development": """
Khóa học Mobile Development giúp học viên xây dựng ứng dụng Android/iOS,
quản lý state, UI components và kết nối API backend.
""",

    "DevOps": """
Khóa học DevOps bao gồm Docker, Kubernetes, CI/CD pipelines, monitoring,
và tự động hóa triển khai phần mềm.
""",

    "Cloud": """
Khóa học Cloud Computing giúp triển khai hệ thống lên AWS, Azure, GCP;
hiểu compute, storage, IAM, networking, autoscaling.
""",

    "Data Science": """
Khóa học Data Science tập trung vào pandas, numpy, thống kê mô tả,
làm sạch dữ liệu, trực quan hóa và xử lý dữ liệu thực tế.
""",

    "AI & ML": """
Khóa học AI & ML cung cấp nền tảng học máy, xử lý dữ liệu,
huấn luyện mô hình, đánh giá accuracy và triển khai AI vào ứng dụng.
""",

    "Cybersecurity": """
Khóa học Cybersecurity tập trung vào bảo mật web, OWASP Top 10,
các kỹ thuật tấn công phổ biến và cách phòng vệ hệ thống.
""",

    "QA / Testing": """
Khóa học Testing bao gồm test case, automation testing, API testing,
performance testing và quy trình đảm bảo chất lượng phần mềm.
""",

    "Tools": """
Khóa học Tools cung cấp kiến thức Git, GitHub, Agile Scrum và các công cụ hỗ trợ phát triển phần mềm.
""",

    "Software Engineering": """
Khóa học SE bao gồm clean code, design patterns, system design và quy trình phát triển phần mềm chuyên nghiệp.
"""
}

# MAPPING CATEGORY → RESOURCES
category_resources_map = {
    "Web Development": [
        "https://developer.mozilla.org/en-US/docs/Web",
        "https://www.w3schools.com/"
    ],
    "Backend Development": [
        "https://www.postman.com/",
        "https://swagger.io/docs/"
    ],
    "Programming": [
        "https://www.programiz.com/",
        "https://www.geeksforgeeks.org/"
    ],
    "Database": [
        "https://www.mongodb.com/docs/",
        "https://www.mysqltutorial.org/"
    ],
    "Mobile Development": [
        "https://developer.android.com/",
        "https://flutter.dev/"
    ],
    "DevOps": [
        "https://docs.docker.com/",
        "https://kubernetes.io/docs/"
    ],
    "Cloud": [
        "https://aws.amazon.com/getting-started/",
        "https://learn.microsoft.com/azure/"
    ],
    "Data Science": [
        "https://pandas.pydata.org/docs/",
        "https://numpy.org/doc/"
    ],
    "AI & ML": [
        "https://scikit-learn.org/stable/",
        "https://www.tensorflow.org/"
    ],
    "Cybersecurity": [
        "https://owasp.org",
        "https://portswigger.net/web-security"
    ],
    "QA / Testing": [
        "https://softwaretestinghelp.com",
        "https://www.guru99.com/testing.html"
    ],
    "Tools": [
        "https://git-scm.com/doc",
        "https://www.atlassian.com/agile"
    ],
    "Software Engineering": [
        "https://martinfowler.com/",
        "https://refactoring.guru/"
    ]
}

# -------------------------------------------------------
# UPDATE LOGIC — GHI ĐÈ GIÁ TRỊ RỖNG
# -------------------------------------------------------

updated = 0

for course in courses.find():
    cat = course.get("category")

    update_data = {}

    # Update theory nếu:
    # - không có field
    # - hoặc rỗng ""
    if "theory" not in course or not course.get("theory"):
        update_data["theory"] = category_theory_map.get(cat, "Nội dung đang được cập nhật.")

    # Update resources nếu:
    # - không có field
    # - hoặc mảng rỗng []
    if "resources" not in course or not course.get("resources"):
        update_data["resources"] = category_resources_map.get(cat, ["https://google.com"])

    # Nếu có update, ghi vào DB
    if update_data:
        courses.update_one({"_id": course["_id"]}, {"$set": update_data})
        updated += 1

print("Đã cập nhật:", updated, "khóa học.")
