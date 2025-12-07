from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from extensions import db
from bson import ObjectId
import os, uuid
from flask import jsonify



admin_teacher_bp = Blueprint("admin_teacher", __name__, url_prefix="/admin/teachers")

# Chặn user thường
@admin_teacher_bp.before_request
def restrict_to_admin():
    if not current_user.is_authenticated or current_user.role != "admin":
        return "Bạn không có quyền truy cập!", 403


# ========== DANH SÁCH GIẢNG VIÊN ==========
@admin_teacher_bp.route("/")
def teacher_list():
    teachers = list(db.teachers.find())
    return render_template("admin/teacher_list.html", teachers=teachers)


# ========== THÊM GIẢNG VIÊN ==========
@admin_teacher_bp.route("/add", methods=["GET", "POST"])
def teacher_add():
    if request.method == "POST":
        name = request.form["name"]
        bio = request.form["bio"]
        avatar_file = request.files.get("avatar")

        avatar_path = "/static/img/teachers/default_teacher.png"

        # nếu có upload avatar
        if avatar_file and avatar_file.filename != "":
            ext = avatar_file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER_TEACHER"], filename)
            avatar_file.save(save_path)
            avatar_path = f"/static/img/teachers/{filename}"

        teacher = {
            "name": name,
            "bio": bio,
            "avatar": avatar_path
        }

        db.teachers.insert_one(teacher)
        flash("Thêm giảng viên thành công!")
        return redirect(url_for("admin_teacher.teacher_list"))

    return render_template("admin/teacher_add.html")


# ========== SỬA GIẢNG VIÊN ==========
@admin_teacher_bp.route("/edit/<tid>", methods=["GET", "POST"])
def teacher_edit(tid):
    teacher = db.teachers.find_one({"_id": ObjectId(tid)})
    if not teacher:
        return "Không tìm thấy giảng viên!", 404

    if request.method == "POST":
        name = request.form["name"]
        bio = request.form["bio"]

        avatar_file = request.files.get("avatar")

        avatar_path = teacher["avatar"]

        # Nếu chọn avatar mới → upload
        if avatar_file and avatar_file.filename != "":
            ext = avatar_file.filename.rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(current_app.config["UPLOAD_FOLDER_TEACHER"], filename)
            avatar_file.save(save_path)
            avatar_path = f"/static/img/teachers/{filename}"

        db.teachers.update_one(
            {"_id": ObjectId(tid)},
            {"$set": {"name": name, "bio": bio, "avatar": avatar_path}}
        )

        flash("Cập nhật giảng viên thành công!")
        return redirect(url_for("admin_teacher.teacher_list"))

    return render_template("admin/teacher_edit.html", teacher=teacher)


# ========== XÓA GIẢNG VIÊN ==========
@admin_teacher_bp.route("/delete/<tid>")
def teacher_delete(tid):
    db.teachers.delete_one({"_id": ObjectId(tid)})
    flash("Đã xóa giảng viên!")
    return redirect(url_for("admin_teacher.teacher_list"))

@admin_teacher_bp.route("/by-category")
def teachers_by_category():
    category = request.args.get("category")

    if not category:
        return jsonify([])

    teachers = list(db.teachers.find({"category": category}))

    for t in teachers:
        t["_id"] = str(t["_id"])

    return jsonify(teachers)
