from flask import Flask, render_template
from extensions import db, login_manager   # lấy từ extensions.py
from routes.recommend_routes import recommend_bp
from routes.learning_path_routes import learning_bp
from routes.profile_routes import profile_bp
from flask import current_app as app
from flask import request
from routes.admin_course_routes import admin_course_bp
from routes.admin_teacher_routes import admin_teacher_bp
from routes.admin_users import admin_users_bp
from routes.admin_stats import admin_stats_bp
import os

app = Flask(__name__)
app.secret_key = "secret-key-change-this"
app.jinja_env.globals['request'] = request
UPLOAD_FOLDER = "static/img/users"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


app.config["UPLOAD_FOLDER"] = "static/img/users"
app.config["UPLOAD_FOLDER_TEACHER"] = "static/img/teachers"


# Khởi tạo login manager
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Import routes SAU KHI khởi tạo app để tránh circular import
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp

app.register_blueprint(auth_bp)
app.register_blueprint(course_bp)
app.register_blueprint(recommend_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(admin_course_bp)
app.register_blueprint(admin_teacher_bp)
app.register_blueprint(admin_users_bp)
app.register_blueprint(admin_stats_bp)

@app.route("/")
def index():
    teachers = list(db.teachers.find().limit(13))
    return render_template("index.html", teachers=teachers)

if __name__ == "__main__":
    app.run(debug=True)
