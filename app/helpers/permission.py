from app.models.user import User
from app.helpers.auth import authenticated
from datetime import time


def check(session, permission):

    return User.has_permission(session.get("user_id"), permission)


