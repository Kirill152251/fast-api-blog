from functools import wraps

from app.tests.logic.conftest import override_get_admin, override_get_current_user 
from app.auth import get_admin, get_current_user
from main import app


def override_get_current_user_get_admin_dep(func):

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            app.dependency_overrides[get_admin] = override_get_admin
            app.dependency_overrides[get_current_user] = override_get_current_user
            func(*args, **kwargs)
        finally:
            app.dependency_overrides[get_admin] = get_admin 
            app.dependency_overrides[get_current_user] = get_current_user
    return inner

