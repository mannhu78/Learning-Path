from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["learning_path"]
courses = db["courses"]

# ======================================================
#  MAPPING: CATEGORY → THEORY (MARKDOWN)
#  Dán nội dung Markdown mà tôi đã tạo vào đây
# ======================================================

category_markdown = {
    "Web Development": """# Web Development

## 1. Giới thiệu Web
- Cách web hoạt động (HTTP Request/Response)
- Client vs Server
- Trình duyệt render HTML/CSS/JS

## 2. HTML
- Cấu trúc HTML
- Semantic HTML
- Forms và Input Types

## 3. CSS
- Box model, Layout
- Flexbox
- Grid
- Responsive

## 4. JavaScript cơ bản
- DOM manipulation
- Event handling
- Fetch API

## 5. UI Frameworks
- Bootstrap
- TailwindCSS

## 6. Best Practices
- SEO
- Performance optimization
""",

    "Backend Development": """# Backend Development

## 1. Backend là gì?
- Vai trò xử lý logic và dữ liệu
- API, microservices

## 2. REST API
- HTTP methods
- Status codes
- Headers, body, params

## 3. Authentication
- Session vs Token
- JWT
- Refresh Token Flow

## 4. Database Integration
- ORM
- Migration
- Validation

## 5. Clean Architecture
- Service layer
- Repository layer

## 6. Security
- Hash password
- SQL injection
- XSS
""",

    "Programming": """# Programming Fundamentals

## 1. Biến & Kiểu dữ liệu
## 2. Hàm
## 3. Cấu trúc điều khiển
## 4. Vòng lặp
## 5. OOP
- Class, Object
- Inheritance
- Encapsulation
- Polymorphism

## 6. Xử lý lỗi (Exception)
## 7. File I/O
## 8. Debugging
""",

    "Database": """# Database Fundamentals

## 1. SQL vs NoSQL
## 2. Thiết kế CSDL
- Tables, Keys
- Normalization

## 3. SQL
- SELECT
- JOIN
- GROUP BY

## 4. MongoDB
- Document
- Collection
- Aggregation Pipeline

## 5. Indexing & Performance
""",

    "Mobile Development": """# Mobile Development

## 1. Native vs Cross-platform

## 2. Android
- Activity
- Fragment
- RecyclerView
- Lifecycle

## 3. iOS
- UIKit
- ViewController

## 4. Flutter
- Widget tree
- State management
- Routing

## 5. API Integration
""",

    "DevOps": """# DevOps

## 1. DevOps Overview
- CI/CD
- Automation

## 2. Docker
- Image
- Container
- Dockerfile

## 3. Kubernetes
- Pod
- Deployment
- Service
- Ingress

## 4. Monitoring
- Prometheus
- Grafana
""",

    "Cloud": """# Cloud Computing

## 1. Cloud Service Models
- IaaS
- PaaS
- SaaS

## 2. AWS Components
- EC2
- S3
- RDS
- IAM

## 3. Networking
- VPC
- Load Balancer
""",

    "Data Science": """# Data Science

## 1. Pandas
- DataFrame
- Cleaning
- Missing values

## 2. Numpy
- Ndarray
- Broadcasting

## 3. Visualization
- Matplotlib
- Seaborn

## 4. Statistics
- Mean, median
- Variance
- Correlation

## 5. EDA
""",

    "AI & ML": """# AI & Machine Learning

## 1. Machine Learning Concepts
- Supervised
- Unsupervised

## 2. Algorithms
- KNN
- Decision Tree
- Random Forest
- Logistic Regression
- SVM

## 3. Deep Learning
- Neural Networks
- CNN
- RNN

## 4. Deployment
- Save model
- API inference
""",

    "Cybersecurity": """# Cybersecurity

## 1. OWASP Top 10
- Injection
- XSS
- CSRF

## 2. Network Security
- Firewall
- VPN

## 3. Cryptography
- Hashing
- Encryption

## 4. Pentesting Tools
- BurpSuite
""",

    "QA / Testing": """# QA / Testing

## 1. Manual Testing
- Test case
- Bug life cycle

## 2. Automation Testing
- Selenium
- Locators

## 3. API Testing
- Postman
- Newman

## 4. Performance Testing
- JMeter
""",

    "Tools": """# Development Tools

## 1. Git
- Commit
- Branch
- Merge
- Rebase

## 2. Scrum
- Sprint
- Daily meeting
""",

    "Software Engineering": """# Software Engineering

## 1. SDLC
## 2. Design Patterns
- Singleton
- Factory
- Adapter
- Strategy

## 3. System Design
- Load balancing
- Caching
- Replication

## 4. Clean Code
- Naming
- Small functions
"""
}

# ======================================================
#  UPDATE 100% COURSE THEORY
# ======================================================

updated = 0

for course in courses.find():
    cat = course.get("category")

    if cat in category_markdown:
        new_md = category_markdown[cat]

        courses.update_one(
            {"_id": course["_id"]},
            {"$set": {"theory": new_md}}
        )
        updated += 1

print("Đã cập nhật:", updated, "khóa học.")
