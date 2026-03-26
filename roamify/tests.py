from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Place, Review

class UserProfileTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='Daniel', password='pass123')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'Daniel')
        self.assertTrue(self.user.check_password('pass123'))

    def test_profile_creation(self):
        profile = Profile.objects.create(user=self.user, bio="Traveler")
        self.assertEqual(profile.user.username, 'Daniel')
        self.assertEqual(profile.bio, "Traveler")

class PlaceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.place = Place.objects.create(
            name="Eiffel Tower",
            description="Famous landmark in Paris",
            location="Paris",
            created_by=self.user
        )

    def test_place_creation(self):
        self.assertEqual(self.place.name, "Eiffel Tower")
        self.assertEqual(self.place.location, "Paris")

    def test_average_rating_no_reviews(self):
        self.assertEqual(self.place.average_rating(), 0)


class ReviewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pass123')
        self.place = Place.objects.create(
            name="Colosseum",
            description="Ancient Roman landmark",
            location="Rome",
            created_by=self.user
        )

    def test_review_creation(self):
        review = Review.objects.create(
            place=self.place,
            user=self.user,
            rating=5,
            comment="Amazing place!"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Amazing place!")

    def test_average_rating(self):
        Review.objects.create(place=self.place, user=self.user, rating=4, comment="Good")
        user2 = User.objects.create_user(username='jane', password='pass123')
        Review.objects.create(place=self.place, user=user2, rating=2, comment="Okay")

        self.assertEqual(self.place.average_rating(), 3)


class viewTest(Testcase):
    
