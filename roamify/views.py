from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import JsonResponse
from django.db.models import Avg
from .models import Place, Review, Comment


def index(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'date')
    category = request.GET.get('category', 'all')

    places = Place.objects.all()

    if query:
        places = places.filter(name__icontains=query) | Place.objects.filter(location__icontains=query)

    if category != 'all':
        places = places.filter(category=category)

    if sort == 'oldest':
        places = places.order_by('created_at')
    elif sort == 'popularity':
        places = places.order_by('-view_count', '-created_at')
    elif sort == 'rating':
        places = places.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating', '-created_at')
    else:
        places = places.order_by('-created_at')

    return render(request, 'roamify/index.html', {
        'places': places,
        'query': query,
        'sort': sort,
        'category': category,
    })


@login_required
def post(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if name and description and location and category:
            Place.objects.create(
                name=name,
                description=description,
                location=location,
                category=category,
                image=image,
                created_by=request.user
            )
            return redirect('roamify:index')

    return render(request, 'roamify/post.html')


def destination(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    # increment views each time page is opened
    place.view_count += 1
    place.save(update_fields=['view_count'])

    reviews = place.reviews.all().order_by('-created_at')
    comments = place.comments.all().order_by('-created_at')

    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(place=place, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        form_type = request.POST.get('form_type')

        if form_type == 'review':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            if rating and comment:
                try:
                    rating = int(rating)
                    if 1 <= rating <= 5:
                        if user_review:
                            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                                return JsonResponse({
                                    'success': False,
                                    'error': 'You have already reviewed this destination.'
                                })
                            return redirect('roamify:destination', place_id=place.id)

                        review = Review.objects.create(
                            place=place,
                            user=request.user,
                            rating=rating,
                            comment=comment
                        )

                        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': True,
                                'username': review.user.username,
                                'rating': review.rating,
                                'comment': review.comment,
                                'created_at': review.created_at.strftime('%b %d, %Y'),
                                'average_rating': f"{place.average_rating():.1f}",
                                'review_count': place.reviews.count(),
                            })

                        return redirect('roamify:destination', place_id=place.id)
                except ValueError:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'error': 'Invalid rating.'
                        })

        elif form_type == 'comment':
            text = request.POST.get('text')

            if text:
                comment_obj = Comment.objects.create(
                    place=place,
                    user=request.user,
                    text=text
                )

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'username': comment_obj.user.username,
                        'text': comment_obj.text,
                        'created_at': comment_obj.created_at.strftime('%b %d, %Y'),
                        'comment_count': place.comments.count(),
                    })

                return redirect('roamify:destination', place_id=place.id)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Comment cannot be empty.'
                })

    return render(request, 'roamify/destination.html', {
        'place': place,
        'reviews': reviews,
        'comments': comments,
        'user_review': user_review,
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('roamify:index')
    else:
        form = UserCreationForm()

    return render(request, 'roamify/signup.html', {'form': form})