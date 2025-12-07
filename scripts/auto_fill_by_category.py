from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
courses = db["courses"]

# ================================
# CATEGORY → TEMPLATE DATA
# ================================
category_templates = {

    "Web Development": {
        "learning_objectives": [
            "Hiểu HTML, CSS, JavaScript",
            "Tạo giao diện web responsive",
            "Làm việc với API và xử lý dữ liệu",
            "Triển khai website lên hosting"
        ],
        "course_outline": [
            {"title": "HTML & CSS", "content": "Thẻ HTML, Layout, Flexbox, Grid"},
            {"title": "JavaScript", "content": "DOM, Event, AJAX, Fetch API"},
            {"title": "Frontend Project", "content": "Xây dựng trang web hoàn chỉnh"}
        ],
        "prerequisites": ["Không yêu cầu kiến thức đầu vào"],
        "target_audience": ["Người mới", "Sinh viên CNTT", "Người chuyển ngành"],
        "instructor": {"name": "Nguyễn Minh H", "bio": "Frontend Engineer 6 năm kinh nghiệm.", "avatar": "/static/img/instructor_web.png"}
    },

    "Backend Development": {
        "learning_objectives": [
            "Hiểu kiến trúc server-side",
            "Xây dựng REST API",
            "Tích hợp database SQL/NoSQL",
            "Xử lý authentication & authorization"
        ],
        "course_outline": [
            {"title": "API cơ bản", "content": "Routing, Middleware, Controller"},
            {"title": "Database", "content": "ORM, Indexing, Transactions"},
            {"title": "Auth", "content": "JWT, OAuth2, Session"}
        ],
        "prerequisites": ["Biết lập trình cơ bản"],
        "target_audience": ["Backend beginner", "Sinh viên năm 2+"],
        "instructor": {"name": "Trần Quốc B", "bio": "Backend Developer tại Shopee.", "avatar": "/static/img/instructor_backend.png"}
    },

    "AI & ML": {
        "learning_objectives": [
            "Hiểu supervised vs unsupervised learning",
            "Tiền xử lý dữ liệu",
            "Huấn luyện mô hình ML cơ bản",
            "Đánh giá model bằng accuracy, precision, recall"
        ],
        "course_outline": [
            {"title": "Machine Learning Basics", "content": "Linear Regression, Classification"},
            {"title": "Data Processing", "content": "Cleaning, Scaling, Feature engineering"},
            {"title": "Model Training", "content": "Train, Test, Evaluation"}
        ],
        "prerequisites": ["Python cơ bản"],
        "target_audience": ["Sinh viên CNTT", "Người vào ngành AI"],
        "instructor": {"name": "Phạm Tuấn A", "bio": "Data Scientist tại VNG.", "avatar": "/static/img/instructor_ai.png"}
    },

    "Data Science": {
        "learning_objectives": [
            "Phân tích dữ liệu với Python",
            "Hiểu thống kê ứng dụng",
            "Xây dựng mô hình dự đoán",
            "Trực quan dữ liệu (Data Visualization)"
        ],
        "course_outline": [
            {"title": "Python for Data", "content": "Pandas, Numpy"},
            {"title": "Visualization", "content": "Matplotlib, Seaborn"},
            {"title": "Modeling", "content": "ML basic models"}
        ],
        "prerequisites": ["Biết Python"],
        "target_audience": ["Data beginner", "Sinh viên CNTT"],
        "instructor": {"name": "Lê Minh Q", "bio": "Senior Data Analyst tại Viettel.", "avatar": "/static/img/instructor_ds.png"}
    },

    "Database": {
        "learning_objectives": [
            "Hiểu SQL & NoSQL",
            "Thiết kế mô hình CSDL",
            "Tối ưu truy vấn",
            "Quản lý index và performance"
        ],
        "course_outline": [
            {"title": "SQL cơ bản", "content": "CRUD, JOIN, GROUP BY"},
            {"title": "NoSQL", "content": "MongoDB, indexing"},
            {"title": "Database Design", "content": "ERD, normalization"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["Sinh viên", "QA/Tester"],
        "instructor": {"name": "Võ Đức T", "bio": "DBA Specialist.", "avatar": "/static/img/instructor_db.png"}
    },

    "Cybersecurity": {
        "learning_objectives": [
            "Hiểu các lỗ hổng phổ biến",
            "Kỹ thuật bảo mật cơ bản",
            "Phòng chống tấn công mạng",
            "Thực hành Pentest cơ bản"
        ],
        "course_outline": [
            {"title": "Security Basics", "content": "Firewall, Encryption"},
            {"title": "Common Attacks", "content": "XSS, SQL Injection"},
            {"title": "Pentest Tools", "content": "Burp Suite, Kali Linux"}
        ],
        "prerequisites": ["Máy tính cơ bản"],
        "target_audience": ["Sinh viên an ninh mạng"],
        "instructor": {"name": "Dương Tấn P", "bio": "Security Engineer tại BIDV.", "avatar": "/static/img/instructor_cyber.png"}
    },

    "Cloud": {
        "learning_objectives": [
            "Hiểu AWS/Azure/GCP cơ bản",
            "Triển khai VM, Storage",
            "Sử dụng Docker trong môi trường cloud"
        ],
        "course_outline": [
            {"title": "Cloud Fundamentals", "content": "Compute, Storage, Networking"},
            {"title": "Deploy App", "content": "EC2, S3, Load Balancer"},
            {"title": "Containers", "content": "Docker, Cloud Run"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["DevOps beginner"],
        "instructor": {"name": "Huỳnh Ngọc S", "bio": "Cloud Engineer tại FPT.", "avatar": "/static/img/instructor_cloud.png"}
    },

    "DevOps": {
        "learning_objectives": [
            "Hiểu CI/CD",
            "Sử dụng Docker",
            "Tự động hoá deploy",
            "Monitoring & Logging"
        ],
        "course_outline": [
            {"title": "CI/CD Pipeline", "content": "GitHub Actions, Jenkins"},
            {"title": "Containers", "content": "Dockerfile, Compose"},
            {"title": "Logging", "content": "Grafana, Prometheus"}
        ],
        "prerequisites": ["Cơ bản lập trình"],
        "target_audience": ["Sinh viên DevOps"],
        "instructor": {"name": "Nguyễn Hoàng K", "bio": "DevOps Engineer tại Vingroup.", "avatar": "/static/img/instructor_devops.png"}
    },

    "Mobile Development": {
        "learning_objectives": [
            "Xây dựng ứng dụng Android/iOS",
            "Làm việc với API",
            "Triển khai ứng dụng mobile"
        ],
        "course_outline": [
            {"title": "UI Mobile", "content": "Widgets, Layouts"},
            {"title": "API Integration", "content": "Fetch API"},
            {"title": "Publish App", "content": "Google Play/App Store"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["Người mới"],
        "instructor": {"name": "Hồ Văn D", "bio": "Mobile Engineer tại MoMo.", "avatar": "/static/img/instructor_mobile.png"}
    },

    "Programming": {
        "learning_objectives": [
            "Hiểu cú pháp ngôn ngữ",
            "Giải quyết vấn đề",
            "Ứng dụng thuật toán cơ bản"
        ],
        "course_outline": [
            {"title": "Syntax & Variables", "content": "Biến, kiểu dữ liệu, toán tử"},
            {"title": "Control Flow", "content": "If, Loop, Function"},
            {"title": "OOP", "content": "Class, Object, Polymorphism"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["Người học lập trình mới"],
        "instructor": {"name": "Nguyễn Vũ M", "bio": "Software Engineer.", "avatar": "/static/img/instructor_programming.png"}
    },

    "QA / Testing": {
        "learning_objectives": [
            "Hiểu quy trình kiểm thử",
            "Viết test case",
            "Kiểm thử thủ công & tự động"
        ],
        "course_outline": [
            {"title": "Manual Testing", "content": "STLC, Test Case, Bug Report"},
            {"title": "Automation", "content": "Selenium basics"},
            {"title": "API Testing", "content": "Postman, Newman"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["Sinh viên QA"],
        "instructor": {"name": "Phạm Tuyết L", "bio": "QA Lead.", "avatar": "/static/img/instructor_qa.png"}
    },

    "Software Engineering": {
        "learning_objectives": [
            "Hiểu vòng đời phát triển phần mềm",
            "Thiết kế kiến trúc phần mềm",
            "Áp dụng thiết kế hướng đối tượng"
        ],
        "course_outline": [
            {"title": "SDLC", "content": "Waterfall, Agile"},
            {"title": "UML", "content": "Use-case, Sequence"},
            {"title": "Design Patterns", "content": "Singleton, Factory"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["Sinh viên IT"],
        "instructor": {"name": "Đào Bảo L", "bio": "Software Architect.", "avatar": "/static/img/instructor_se.png"}
    },

    "Tools": {
        "learning_objectives": [
            "Sử dụng công cụ hỗ trợ dev",
            "Quản lý source code với Git",
            "Tự động hoá công việc"
        ],
        "course_outline": [
            {"title": "Git & GitHub", "content": "Branch, Merge"},
            {"title": "VSCode", "content": "Extensions, Debugging"},
            {"title": "CLI Tools", "content": "Cmd, Bash"}
        ],
        "prerequisites": ["Không yêu cầu"],
        "target_audience": ["Người mới"],
        "instructor": {"name": "Hạnh B", "bio": "Tech Manager.", "avatar": "/static/img/instructor_tools.png"}
    }
}

# APPLY TEMPLATE
updated_count = 0

for course in courses.find():

    cat = course.get("category")

    if cat in category_templates:
        t = category_templates[cat]

        db.courses.update_one(
            {"_id": course["_id"]},
            {"$set": {
                "learning_objectives": t["learning_objectives"],
                "course_outline": t["course_outline"],
                "prerequisites": t["prerequisites"],
                "target_audience": t["target_audience"],
                "instructor": t["instructor"]
            }}
        )
        updated_count += 1

print(f"✔ Đã cập nhật {updated_count} khóa học theo category!")
