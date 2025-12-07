from flask import Blueprint, app, render_template, request,url_for, redirect, flash
from flask_login import login_required, current_user
from extensions import db
from bson import ObjectId


admin_users_bp = Blueprint("admin_users", __name__, url_prefix="/admin/users")


def admin_required():
    return current_user.is_authenticated and current_user.role == "admin"


@admin_users_bp.route("/")
@login_required
def list_users():

    if not admin_required():
        return "Bạn không có quyền truy cập!", 403

    role = request.args.get("role")
    domain = request.args.get("domain")
    keyword = request.args.get("keyword")

    # FIX keyword "None"
    if keyword in (None, "", "None"):
        keyword = None

    query = {}

    # ROLE
    if role not in (None, "", "all"):
        query["role"] = {"$regex": f"^{role}$", "$options": "i"}

    # DOMAIN
    if domain not in (None, "", "all"):
        query["domain"] = {"$regex": f"^{domain}$", "$options": "i"}

    # KEYWORD
    if keyword:
        query["$or"] = [
            {"username": {"$regex": keyword, "$options": "i"}},
            {"goal": {"$regex": keyword, "$options": "i"}}
        ]

    users = list(db.users.find(query, {"password_hash": 0}))

    roles = ["admin", "user"]
    domains = [d for d in db.users.distinct("domain") if d not in ("", None)]

    return render_template(
        "admin/users_list.html",
        users=users,
        roles=roles,
        domains=domains
    )


@admin_users_bp.route("/<user_id>")
@login_required
def user_detail(user_id):
    if not admin_required():
        return "Bạn không có quyền truy cập!", 403

    user = db.users.find_one({"_id": ObjectId(user_id)}, {"password_hash": 0})
    if not user:
        return "Không tìm thấy người dùng.", 404

    # Lấy danh sách khoá học đã lưu
    saved = []
    for cid in user.get("saved_courses", []):
        try:
            c = db.courses.find_one({"_id": ObjectId(cid)})
            if c:
                saved.append(c)
        except:
            pass

    return render_template("admin/user_detail.html", user=user, saved_courses=saved)

@admin_users_bp.route("/delete/<user_id>")
@login_required
def delete_user(user_id):

    if not admin_required():
        return "Bạn không có quyền truy cập!", 403

    # Không cho admin tự xóa chính mình
    if str(current_user.id) == str(user_id):
        flash("Bạn không thể tự xóa tài khoản của chính mình!")
        return redirect(url_for("admin_users.list_users"))

    try:
        db.users.delete_one({"_id": ObjectId(user_id)})
        flash("Xóa người dùng thành công!")
    except Exception as e:
        print("Delete error:", e)
        flash("Không thể xóa người dùng!")

    return redirect(url_for("admin_users.list_users"))