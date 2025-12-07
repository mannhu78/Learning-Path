from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from bson import ObjectId
from extensions import db
from flask import request
admin_course_bp = Blueprint("admin_course", __name__, url_prefix="/admin/courses")

# Chỉ admin được truy cập
@admin_course_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated or current_user.role != "admin":
        return "Bạn không có quyền truy cập!", 403


# DANH SÁCH KHÓA HỌC
@admin_course_bp.route("/")
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
        "admin/course_list.html",
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



# THÊM KHÓA HỌC
@admin_course_bp.route("/add", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":

        instructor_id = request.form.get("instructor_id")

        data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "category": request.form["category"],
            "difficulty": request.form["difficulty"],
            "duration_weeks": int(request.form["duration_weeks"]),
            "skills_required": [s.strip().lower() for s in request.form["skills_required"].split(",")],
            "theory": request.form["theory"],
            "resources": [r.strip() for r in request.form["resources"].split("\n") if r.strip()]
        }

        # LƯU instructor_id nếu có chọn
        if instructor_id:
            data["instructor_id"] = ObjectId(instructor_id)

        db.courses.insert_one(data)
        flash("Thêm khóa học thành công!")
        return redirect(url_for("admin_course.course_list"))

    categories = db.courses.distinct("category")
    teachers = list(db.teachers.find({}))

    return render_template(
        "admin/course_add.html",
        categories=categories,
        teachers=teachers
    )



# SỬA KHÓA HỌC
@admin_course_bp.route("/edit/<cid>", methods=["GET", "POST"])
def edit_course(cid):
    course = db.courses.find_one({"_id": ObjectId(cid)})
    if not course:
        return "Không tìm thấy khóa học!", 404

    if request.method == "POST":

        instructor_id = request.form.get("instructor_id")
        if instructor_id:
            instructor_id = ObjectId(instructor_id)
        else:
            instructor_id = None

        update_data = {
            "title": request.form["title"],
            "description": request.form["description"],
            "category": request.form["category"],
            "difficulty": request.form["difficulty"],
            "duration_weeks": int(request.form["duration_weeks"]),
            "skills_required": [
                s.strip().lower() for s in request.form["skills_required"].split(",") if s.strip()
            ],
            "theory": request.form["theory"],
            "resources": [
                r.strip() for r in request.form["resources"].split("\n") if r.strip()
            ],
            "instructor_id": instructor_id
        }

        db.courses.update_one({"_id": ObjectId(cid)}, {"$set": update_data})
        flash("Cập nhật khóa học thành công!")
        return redirect(url_for("admin_course.course_list"))

    # ============ GET MODE: Render Form ============

    categories = db.courses.distinct("category")
    teachers = list(db.teachers.find({}))

    # text resource
    resources_text = "\n".join(course.get("resources", []))

    return render_template(
        "admin/course_edit.html",
        course=course,
        resources_text=resources_text,
        categories=categories,
        teachers=teachers
    )


# XÓA KHÓA HỌC
@admin_course_bp.route("/delete/<cid>")
def delete_course(cid):
    db.courses.delete_one({"_id": ObjectId(cid)})
    flash("Đã xóa khóa học.")
    return redirect(url_for("admin_course.course_list"))
