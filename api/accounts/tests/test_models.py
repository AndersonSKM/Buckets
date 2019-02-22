import pytest

from accounts.models import User


class TestUser:
    @pytest.fixture
    def user(self):
        return User(email='test@test.com', name='John Doe')

    def test_str(self, user):
        assert str(user) == user.email

    def test_clean_superuser_set_is_staff_true(self, user):
        user.is_staff = False
        user.is_superuser = True
        user.clean()

        assert user.is_staff
        assert user.is_superuser

    def test_email_user(self, user, mailoutbox):
        user.email_user(subject='this is an important email', message='test')
        assert len(mailoutbox) == 1

        mail = mailoutbox[0]
        assert mail.subject == 'this is an important email'
        assert mail.body == 'test'
        assert mail.to == [user.email]
