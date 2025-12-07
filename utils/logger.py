from datetime import datetime
from extensions import db
from flask_login import current_user

def log_action(action, meta=None):
    db.user_logs.insert_one({
        "user_id": str(current_user.get_id()) if current_user.is_authenticated else None,
        "action": action,
        "meta": meta,
        "timestamp": datetime.utcnow()
    })
