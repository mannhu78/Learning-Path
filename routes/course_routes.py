from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db
from flask_login import login_required, current_user
from bson import ObjectId
from utils.logger import log_action
import markdown

course_bp = Blueprint("course", __name__, url_prefix="/courses")

# ==========================
# LIST + FILTER + PAGINATION
# ==========================
@course_bp.route("/")
def course_list():
    category = request.args.get("category")
    difficulty = request.args.get("difficulty")
    keyword = request.args.get("keyword")
    skill = request.args.get("skill")
    instructor = request.args.get("instructor")

    if not keyword or keyword == "None":
        keyword = None

    # Pagination
    page = int(request.args.get("page", 1))
    per_page = 10
    skip = (page - 1) * per_page

    query = {}

    if category and category != "all":
        query["category"] = category

    if difficulty and difficulty != "all":
        query["difficulty"] = difficulty

    if skill and skill != "all":
        query["skills_required"] = {"$in": [skill.lower()]}

    if instructor and instructor != "all":
        try:
            query["instructor_id"] = ObjectId(instructor)
        except:
            pass

    if keyword:
        query["$or"] = [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}}
        ]

    total_courses = db.courses.count_documents(query)
    courses = list(db.courses.find(query).skip(skip).limit(per_page))
    
    total_pages = (total_courses + per_page - 1) // per_page

    all_categories = db.courses.distinct("category")
    all_skills_raw = db.courses.distinct("skills_required")

    flattened_skills = sorted({
    skill
    for item in all_skills_raw
    for skill in (item if isinstance(item, list) else [item])
    })



    teachers = list(db.teachers.find())

    return render_template(
        "courses_list.html",
        courses=courses,
        all_categories=all_categories,
        all_skills=flattened_skills,
        teachers=teachers,
        page=page,
        total_pages=total_pages,
        total_courses=total_courses,
        per_page=per_page,
        selected_instructor=instructor
    )

# ==========================
# ADD COURSE
# ==========================
@course_bp.route("/add", methods=["GET", "POST"])
@login_required
def course_add():
    if current_user.role != "admin":
        return "Bạn không có quyền truy cập!", 403

    if request.method == "POST":

        resources_raw = request.form.get("resources", "")
        resources_list = [r.strip() for r in resources_raw.split("\n") if r.strip()]

        instructor_id = request.form.get("instructor_id")
        if instructor_id:
            instructor_id = ObjectId(instructor_id)

        data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "skills_required": [
                s.strip().lower() for s in request.form.get("skills_required", "").split(",") if s.strip()
            ],
            "difficulty": request.form["difficulty"],
            "duration_weeks": int(request.form["duration_weeks"]),
            "category": request.form["category"],
            "theory": request.form.get("theory", ""),
            "resources": resources_list,
            "instructor_id": instructor_id
        }

        db.courses.insert_one(data)
        return redirect(url_for("course.course_list"))

    teachers = list(db.teachers.find())
    return render_template("course_add.html", teachers=teachers)


# ==========================
# COURSE DETAIL  (ĐÃ FIX)
# ==========================
@course_bp.route("/<cid>")
def course_detail(cid):

    try:
        cid = ObjectId(cid)
    except:
        return "ID không hợp lệ", 404

    course = db.courses.find_one({"_id": cid})
    if not course:
        return "Không tìm thấy khóa học", 404

    # LOAD GIẢNG VIÊN
    instructor = None
    if course.get("instructor_id"):
        instructor = db.teachers.find_one({"_id": course["instructor_id"]})

    # LOG + SAVED COURSES
    saved_ids = []
    if current_user.is_authenticated:
        log_action("view_course", {"course_id": cid})
        saved_ids = [str(id) for id in getattr(current_user, "saved_courses", [])]

    # CHUYỂN MARKDOWN -> HTML
    theory_html = markdown.markdown(course.get("theory", ""))

    return render_template(
        "course_detail.html",
        course=course,
        instructor=instructor,
        saved_ids=saved_ids,
        theory_html=theory_html
    )

