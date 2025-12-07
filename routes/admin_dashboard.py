from flask import Blueprint, render_template
from flask_login import login_required, current_user
from extensions import db
from bson import ObjectId

admin_stats_bp = Blueprint("admin_stats", __name__, url_prefix="/admin")

def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"

@admin_stats_bp.before_request
def restrict_admin():
    if not admin_required():
        return "Bạn không có quyền truy cập!", 403


@admin_stats_bp.route("/")
def dashboard():

    # Tổng quan
    total_users = db.users.count_documents({})
    total_courses = db.courses.count_documents({})
    total_categories = len(db.courses.distinct("category"))

    # HEATMAP
    pipeline_heatmap = [
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$updated_at"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}}
    ]

    heatmap_data = list(db.users.aggregate(pipeline_heatmap))

    if not heatmap_data:
        heatmap_data = [
            {"_id": "2025-12-01", "count": 2},
            {"_id": "2025-12-02", "count": 4},
            {"_id": "2025-12-03", "count": 6},
        ]

    # HOT COURSES
    pipeline_hot_courses = [
        {"$unwind": "$saved_courses"},
        {
            "$group": {
                "_id": "$saved_courses",
                "saves": {"$sum": 1}
            }
        },
        {"$sort": {"saves": -1}},
        {"$limit": 5}
    ]

    raw = list(db.users.aggregate(pipeline_hot_courses))
    hot_courses = []

    for item in raw:
        try:
            c = db.courses.find_one({"_id": ObjectId(item["_id"])})
            if c:
                hot_courses.append({
                    "title": c["title"],
                    "saves": item["saves"]
                })
        except:
            pass

    if not hot_courses:
        hot_courses = [{"title": "Chưa có dữ liệu", "saves": 0}]

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_courses=total_courses,
        total_categories=total_categories,
        heatmap_data=heatmap_data,
        hot_courses=hot_courses
    )
