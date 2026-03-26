from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Place, Review

def index(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'date')
    category = request.GET.get('category', 'all')

    places = Place.objects.all()

    if query:
        places = places.filter(name__icontains=query)

    if sort == 'oldest':
        places = places.order_by('created_at')
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
        image = request.FILES.get('image')

        Place.objects.create(
            name=name,
            description=description,
            location=location,
            image=image,
            created_by=request.user
        )

        return redirect('roamify:index')

    return render(request, 'roamify/post.html')

def destination(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    reviews = place.reviews.all().order_by('-created_at')

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating and comment:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    Review.objects.create(
                        place=place,
                        user=request.user,
                        rating=rating,
                        comment=comment
                    )
                    return redirect('roamify:destination', place_id=place.id)
            except ValueError:
                pass

    return render(request, 'roamify/destination.html', {
        'place': place,
        'reviews': reviews
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