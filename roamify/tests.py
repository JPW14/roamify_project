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


class viewTest(Testcase
    #index tests
    def test_index_loads(self):
        response = self.client.get(reverse('roamify:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_search(self):
        response = self.client.get(reverse('roamify:index'), {'q': 'Eiffel'})
        self.assertContains(response, "Eiffel Tower")

    def test_index_filter_category(self):
        response = self.client.get(reverse('roamify:index'), {'category': 'landmark'})
        self.assertContains(response, "Eiffel Tower")

    def test_index_sort_oldest(self):
        response = self.client.get(reverse('roamify:index'), {'sort': 'oldest'})
        self.assertEqual(response.status_code, 200)

    def test_index_sort_rating(self):
        Review.objects.create(place=self.place, user=self.user, rating=5, comment="Great")
        response = self.client.get(reverse('roamify:index'), {'sort': 'rating'})
        self.assertEqual(response.status_code, 200)
    #post tests
    def test_post_requires_login(self):
        response = self.client.get(reverse('roamify:post'))
        self.assertEqual(response.status_code, 302) 

    def test_post_create_place(self):
        self.client.login(username='user1', password='pass123')

        response = self.client.post(reverse('roamify:post'), {
            'name': 'Colosseum',
            'description': 'Ancient Rome',
            'location': 'Italy',
            'category': 'history'
        })

        self.assertEqual(Place.objects.count(), 2)
        self.assertRedirects(response, reverse('roamify:index'))

    def test_post_missing_fields(self):
        self.client.login(username='user1', password='pass123')

        response = self.client.post(reverse('roamify:post'), {
            'name': '',
            'description': '',
        })

        self.assertEqual(Place.objects.count(), 1) 
    #Destination tests
    def test_destination_loads(self):
        response = self.client.get(reverse('roamify:destination', args=[self.place.id]))
        self.assertEqual(response.status_code, 200)

    def test_destination_view_count_increment(self):
        self.client.get(reverse('roamify:destination', args=[self.place.id]))
        self.place.refresh_from_db()
        self.assertEqual(self.place.view_count, 1)

    def test_destination_invalid_place(self):
        response = self.client.get(reverse('roamify:destination', args=[999]))
        self.assertEqual(response.status_code, 404)
    #comment tests
    def test_add_comment(self):
        self.client.login(username='user1', password='pass123')

        response = self.client.post(
            reverse('roamify:destination', args=[self.place.id]),
            {
                'form_type': 'comment',
                'text': 'Nice place'
            }
        )

        self.assertEqual(Comment.objects.count(), 1)

    def test_empty_comment(self):
        self.client.login(username='user1', password='pass123')

        response = self.client.post(
            reverse('roamify:destination', args=[self.place.id]),
            {
                'form_type': 'comment',
                'text': ''
            }
        )

        self.assertEqual(Comment.objects.count(), 0)


