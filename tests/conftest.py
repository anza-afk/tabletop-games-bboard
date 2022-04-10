from webapp.user.models import User, UserProfile
from werkzeug.security import generate_password_hash
import pytest


@pytest.fixture(scope='module')
def new_user():
    user = User(
        username='test_user_01',
        password=generate_password_hash('00000'),
        email='testuser01@mail.ru',
        role='1'
    )
    return user
