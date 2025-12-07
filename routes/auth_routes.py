from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, UserMixin,current_user
from extensions import db, login_manager
from bson import ObjectId
from utils.logger import log_action

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.role = user_doc.get("role", "user")
        self.skills = user_doc.get("skills", [])
        self.goal = user_doc.get("goal", "")
        self.domain = user_doc.get("domain", "")
        self.avatar = user_doc.get("avatar")

        # QUAN TRỌNG
        self.saved_courses = user_doc.get("saved_courses", [])

@login_manager.user_loader
def load_user(user_id):
    user_doc = db.users.find_one({"_id": ObjectId(user_id)})
    if user_doc:
        return User(user_doc)
    return None


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if db.users.find_one({"username": username}):
            flash("Username đã tồn tại!")
            return redirect(url_for("auth.register"))

        user = {
            "username": username,
            "password_hash": generate_password_hash(password),
            "role": "user"
        }
        db.users.insert_one(user)
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_doc = db.users.find_one({"username": username})
        if not user_doc or not check_password_hash(user_doc["password_hash"], password):
            flash("Sai thông tin đăng nhập!")
            return redirect(url_for("auth.login"))

        user = User(user_doc)
        login_user(user)
        log_action("login", {"username": user.username})

        # Nếu là admin => chuyển sang trang quản trị
        if user.role == "admin":
            return redirect(url_for("admin_stats.dashboard"))

        # Nếu là user bình thường
        return redirect(url_for("index"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    # Lấy user hiện tại từ DB
    user_doc = db.users.find_one({"_id": ObjectId(current_user.id)})

    if request.method == "POST":
        # Lấy dữ liệu từ form
        skills_raw = request.form.get("skills", "")
        goal = request.form.get("goal", "")
        domain = request.form.get("domain", "")

        skills_list = [s.strip().lower() for s in skills_raw.split(",")] if skills_raw else []

        db.users.update_one(
            {"_id": ObjectId(current_user.id)},
            {
                "$set": {
                    "skills": skills_list,
                    "goal": goal,
                    "domain": domain
                }
            }
        )

        # Lấy lại dữ liệu mới để hiển thị
        user_doc = db.users.find_one({"_id": ObjectId(current_user.id)})
        flash("Cập nhật hồ sơ thành công!")

    # Chuẩn bị dữ liệu string để đưa lên form
    skills_str = ", ".join(user_doc.get("skills", [])) if user_doc.get("skills") else ""

    return render_template(
        "profile.html",
        user=user_doc,
        skills_str=skills_str
    )

