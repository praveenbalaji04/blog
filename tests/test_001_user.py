import pytest
from core.models import User


class TestClass:
    def test_000_delete_users(self):
        for t in User.objects:
            t.delete()
            assert 1 == 1

    def test_001_create_user(self):
        admin_user = User.add_user("admin_user", "test", "admin")
        staff_user = User.add_user('staff_user', 'test', 'staff')

        user = User.objects(name='admin_user').first()
        assert user.name == admin_user.name
        assert user.group == 'admin'
