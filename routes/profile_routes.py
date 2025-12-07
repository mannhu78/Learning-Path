from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from extensions import db
from bson import ObjectId
import datetime
from flask import request
import os
import uuid

from utils.logger import log_action

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@profile_bp.route("")
@login_required
def profile_redirect():
    return redirect(url_for("profile.view_profile"))


@profile_bp.route("/")
@login_required
def view_profile():
    user = db.users.find_one({"_id": ObjectId(current_user.id)})

    saved_course_docs = []
    if "saved_courses" in user:
        for cid in user["saved_courses"]:
            try:
                course = db.courses.find_one({"_id": ObjectId(cid)})
                if course:
                    saved_course_docs.append(course)
            except:
                pass

    return render_template(
        "profile.html",
        user=user,
        saved_courses=saved_course_docs
    )

@profile_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    user = db.users.find_one({"_id": ObjectId(current_user.id)})

    if request.method == "POST":
        data = {
            "about": request.form.get("about"),
            "goal": request.form.get("goal"),
            "domain": request.form.get("domain"),
            "skills": [s.strip().lower() for s in request.form.get("skills").split(",")],
            "updated_at": datetime.datetime.utcnow()
        }

        db.users.update_one({"_id": user["_id"]}, {"$set": data})

        flash("Cập nhật hồ sơ thành công!")
        return redirect(url_for("profile.view_profile"))

    # Render form edit với dữ liệu user
    skills_str = ", ".join(user.get("skills", []))
    return render_template("profile_edit.html", user=user, skills_str=skills_str)

@profile_bp.route("/upload-avatar", methods=["POST"])
@login_required
def upload_avatar():
    if "avatar" not in request.files:
        flash("Không tìm thấy file upload.")
        return redirect(url_for("profile.view_profile"))

    file = request.files["avatar"]

    if file.filename == "":
        flash("Bạn chưa chọn file.")
        return redirect(url_for("profile.view_profile"))

    if not allowed_file(file.filename):
        flash("Chỉ hỗ trợ file PNG, JPG, JPEG.")
        return redirect(url_for("profile.view_profile"))

    # Tạo tên file unique
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"

    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # Update MongoDB
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": {"avatar": f"/static/img/users/{filename}"}}
    )

    flash("Cập nhật ảnh đại diện thành công!")
    return redirect(url_for("profile.view_profile"))

@profile_bp.route("/save-course/<cid>")
@login_required
def save_course(cid):
    db.users.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$addToSet": {"saved_courses": cid}}
    )
    flash("Đã lưu khóa học!")
    log_action("save_course", {"course_id": cid})
    return redirect(url_for("course.course_detail", cid=cid))


@profile_bp.route("/unsave-course/<cid>")
@login_required
def unsave_course(cid):
    try:
        db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$pull": {"saved_courses": cid}}
        )
        log_action("unsave_course", {"course_id": cid})
        flash("Đã bỏ lưu khóa học.")
    except:
        flash("Có lỗi xảy ra.")

    return redirect(url_for("course.course_detail", cid=cid))

