from django.test import TestCase
from django.contrib.auth.models import User

class UserTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='Daniel', password='pass123')
        self.assertTrue(user.check_password('pass123'))


