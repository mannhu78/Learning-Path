from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db
from bson import ObjectId
from ml.recommender import recommend_courses

learning_bp = Blueprint("learning", __name__, url_prefix="/learning-path")

@learning_bp.route("/")
@login_required
def learning_path():
    # Lấy user thông tin
    user_doc = db.users.find_one({"_id": ObjectId(current_user.id)})
    if not user_doc:
        return "Không tìm thấy user!", 404

    user_goal = user_doc.get("goal", "")
    user_skills = user_doc.get("skills", [])

    # Lấy tất cả khóa học
    courses = list(db.courses.find())
    if not courses:
        return "Chưa có khóa học nào."

    # Gọi recommender
    sorted_indexes, scores = recommend_courses(user_goal, user_skills, courses)

    # Lấy top 5 khóa phù hợp nhất
    top_courses = []
    for idx in sorted_indexes[:5]:
        c = courses[idx]
        c["score"] = float(scores[idx])

        # Đảm bảo các trường không bị thiếu
        c["_id"] = str(c["_id"])
        c["skills_required"] = c.get("skills_required", [])
        c["duration_weeks"] = c.get("duration_weeks", 1)

        top_courses.append(c)

    # Tạo lộ trình học (timeline theo khóa, không chia theo tuần lặp lại)
    timeline = []
    current_week = 1

    for course in top_courses:
        timeline.append({
            "_id": course["_id"],
            "week": current_week,
            "title": course["title"],
            "description": course["description"],
            "difficulty": course["difficulty"],
            "category": course["category"],
            "skills_required": course["skills_required"],
            "duration_weeks": course["duration_weeks"]
        })

        # Sau khi xong khóa học → tăng tuần tương ứng
        current_week += course["duration_weeks"]

    return render_template("learning_path.html", timeline=timeline)
