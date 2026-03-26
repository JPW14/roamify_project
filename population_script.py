import os
import django

from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roamify_project.settings')
django.setup()

from django.contrib.auth.models import User
from roamify.models import Profile, Place, Review, Comment


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA_DIR = os.path.join(BASE_DIR, 'sample_data')


def get_image_path(filename):
    return os.path.join(SAMPLE_DATA_DIR, filename)


def clear_data():
    print("Clearing old data...")

    Comment.objects.all().delete()
    Review.objects.all().delete()
    Place.objects.all().delete()
    Profile.objects.all().delete()

    User.objects.filter(username__in=[
        'alice', 'bob', 'clara', 'daniel'
    ]).delete()

    print("Old data cleared.")


def create_user(username, password, bio=""):
    user = User.objects.create_user(username=username, password=password)

    profile = Profile.objects.create(user=user, bio=bio)

    return user


def create_place(name, description, location, category, created_by, image_filename=None):
    place = Place.objects.create(
        name=name,
        description=description,
        location=location,
        category=category,
        created_by=created_by,
    )

    if image_filename:
        image_path = get_image_path(image_filename)
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                place.image.save(image_filename, File(f), save=True)
        else:
            print(f"Warning: image file not found: {image_path}")

    return place


def create_review(place, user, rating, comment):
    return Review.objects.create(
        place=place,
        user=user,
        rating=rating,
        comment=comment,
    )


def create_comment(place, user, text):
    return Comment.objects.create(
        place=place,
        user=user,
        text=text,
    )


def populate():
    print("Populating Roamify data...")

    clear_data()

    alice = create_user("alice", "pass123", "Loves city breaks and food trips.")
    bob = create_user("bob", "pass123", "Beach fan and sunset chaser.")
    clara = create_user("clara", "pass123", "Nature lover and photographer.")
    daniel = create_user("daniel", "pass123", "Enjoys landmarks and historic cities.")

    paris = create_place(
        name="Eiffel Tower",
        description="A famous landmark in Paris with amazing views and iconic architecture.",
        location="Paris, France",
        category="landmarks",
        created_by=daniel,
        image_filename="eiffel.jpg"
    )

    tokyo = create_place(
        name="Tokyo Night Streets",
        description="A vibrant urban destination full of food, lights and nightlife.",
        location="Tokyo, Japan",
        category="urban",
        created_by=alice,
        image_filename="tokyo.jpg"
    )

    bali = create_place(
        name="Bali Beach Paradise",
        description="A relaxing beach destination with clear water and beautiful sunsets.",
        location="Bali, Indonesia",
        category="beach",
        created_by=bob,
        image_filename="bali.jpg"
    )

    tromso = create_place(
        name="Northern Lights Escape",
        description="A peaceful nature getaway and one of the best places to see the aurora.",
        location="Tromsø, Norway",
        category="nature",
        created_by=clara,
        image_filename="tromso.jpg"
    )

    create_review(paris, alice, 5, "Absolutely stunning in person.")
    create_review(paris, bob, 3, "Very busy, but still worth visiting.")

    create_review(tokyo, bob, 5, "Loved the atmosphere and food.")
    create_review(tokyo, clara, 4, "A bit overwhelming at first, but unforgettable.")

    create_review(bali, alice, 2, "Too touristy.")
    create_review(bali, daniel, 5, "Perfect holiday destination.")

    create_review(tromso, alice, 5, "The scenery was incredible.")
    create_review(tromso, bob, 1, "Its way too cold!!!")

    create_comment(paris, clara, "This is high on my travel list.")
    create_comment(paris, daniel, "Go early if you want fewer crowds.")

    create_comment(tokyo, alice, "I want to go back already.")
    create_comment(tokyo, daniel, "The night views look amazing.")

    create_comment(bali, clara, "Looks so peaceful.")
    create_comment(bali, bob, "Sunsets here are unreal.")

    create_comment(tromso, daniel, "Would love to see the northern lights one day.")
    create_comment(tromso, clara, "Best trip I have done in years.")

    print("Done.")


if __name__ == '__main__':
    populate()