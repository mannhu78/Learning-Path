from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db
from bson import ObjectId
from ml.recommender import recommend_courses

recommend_bp = Blueprint("recommend", __name__, url_prefix="/recommend")

@recommend_bp.route("/")
@login_required
def recommend():
    # Lấy user hiện tại từ DB
    user_doc = db.users.find_one({"_id": ObjectId(current_user.id)})

    # Kiểm tra xem user đã có hồ sơ chưa
    if not user_doc.get("skills") or not user_doc.get("goal"):
        return "Bạn cần cập nhật 'skills' và 'goal' trong hồ sơ trước khi xem gợi ý!"

    user_goal = user_doc.get("goal", "")
    user_skills = user_doc.get("skills", [])

    # Lấy toàn bộ khóa học từ MongoDB
    courses = list(db.courses.find())

    # Nếu chưa có khóa học thì không thể recommend
    if not courses:
        return "Chưa có khóa học nào trong hệ thống."

    # Gọi module ML
    sorted_indexes, scores = recommend_courses(user_goal, user_skills, courses)

    # Lấy top 5 khóa học phù hợp nhất
    top_courses = []
    for idx in sorted_indexes[:5]:
        c = courses[idx]
        c["score"] = round(float(scores[idx]), 3)
        top_courses.append(c)

    return render_template("recommend_list.html", courses=top_courses)
