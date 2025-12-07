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

    # ============================
    #        HOẠT ĐỘNG USER
    # ============================
    pipeline_logs = [
        {
            "$group": {
                "_id": {
                    "day": {"$dateToString": {"format": "%Y-%m-%d", "date": "$timestamp"}},
                    "action": "$action"
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.day": 1}}
    ]

    raw_logs = list(db.user_logs.aggregate(pipeline_logs))

    # Convert về dạng ApexCharts cần
    heatmap_data = {}
    for log in raw_logs:
        day = log["_id"]["day"]
        action = log["_id"]["action"]
        count = log["count"]

        if day not in heatmap_data:
            heatmap_data[day] = {}

        heatmap_data[day][action] = count

    # Chuyển thành list cho frontend
    final_logs = []
    for day, actions in heatmap_data.items():
        final_logs.append({
            "day": day,
            "actions": actions,
            "total": sum(actions.values())
        })

    # ============================
    #   TOP COURSE SAVED
    # ============================
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

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_courses=total_courses,
        total_categories=total_categories,
        heatmap_data=final_logs,
        hot_courses=hot_courses
    )
