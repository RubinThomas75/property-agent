from sqlalchemy.orm import Session
from app.models.user import User
import datetime

def get_or_create_user(user_info: dict, db: Session):
    """Retrieves or creates a new user in the database."""
    user_id = user_info["sub"]  # Google stable user ID
    email = user_info["email"]
    name = user_info.get("name", "")
    picture = user_info.get("picture", "")

    user = db.query(User).filter(User.user_id == user_id).first()

    if not user:
        # Create new user
        user = User(user_id=user_id, email=email, name=name, picture=picture)
        db.add(user)
    else:
        # Update last login timestamp
        user.last_logged_in = datetime.datetime.utcnow()

    db.commit()
    db.refresh(user)
    return user
