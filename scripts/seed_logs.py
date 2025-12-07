# scripts/seed_logs.py
from datetime import datetime, timedelta
from extensions import db
from utils.logger import log_action

def seed():
    # tạo 7 ngày dữ liệu mẫu
    today = datetime.utcnow().date()
    for i in range(7):
        d = today - timedelta(days=6-i)
        # insert 1..5 logs/ngày
        for j in range(i % 5 + 1):
            db.user_logs.insert_one({
                "user_id": "seed_user",
                "action": "view_course",
                "meta": {"course_id": "sample"},
                "date": d.strftime("%Y-%m-%d"),
                "timestamp": datetime.combine(d, datetime.min.time())
            })

if __name__ == "__main__":
    seed()
    print("seeded logs")
