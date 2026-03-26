from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import Place

def index(request):
    places = Place.objects.all()
    return render(request, 'roamify/index.html', {'places': places})

@login_required
def post(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        location = request.POST.get('location')

        Place.objects.create(
            name=name,
            description=description,
            location=location,
            created_by=request.user
        )

        return redirect('roamify:index')

    return render(request, 'roamify/post.html')

def destination(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    reviews = place.reviews.all()

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
