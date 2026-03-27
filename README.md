# roamify_project

Roamify is a Django web application where users can share travel destinations, browse places posted by others, leave ratings and reviews, and comment on destination pages.

## Features

- User sign up, login and logout
- User profile editing
- Profile picture upload
- Create and upload travel destinations
- Browse all destinations on the homepage
- Search destinations by name or location
- Filter destinations by category
- Sort destinations by date, popularity, or rating
- View destination details
- Submit one review per user per destination
- Submit multiple comments on destination pages
- AJAX review and comment submission

## Built With

- Python
- Django
- HTML
- CSS
- JavaScript
- AJAX

## Setup Instructions

### 1. Clone the repository

git clone (https://github.com/JPW14/roamify_project.git)
cd roamify_project

### 2. Create and activate a virtutal envrionment

conda create -n roamify python=3.8
conda activate roamify

### 3. Install dependencies

pip install -r requirements.txt

### 4. Run migrations

python manage.py makemigrations
python manage.py migrate

### 5. Populate the database with sample data

python population_script.py

### 6. Run the development server

python manage.py runserver

# Then open:

http://127.0.0.1:8000/


## Sample User Accounts

The population script creates these example users:

Username: alice | Password: pass123
Username: bob | Password: pass123
Username: clara | Password: pass123
Username: daniel | Password: pass123


## External Sources Used

- Django Documentation — used for guidance on models, authentication, forms, views, and file uploads
- MDN Web Docs — used for HTML, CSS, JavaScript, and Fetch API reference
- Pillow Documentation — used for image handling in Django
- PythonAnywhere Documentation — used for deployment guidance
- CSS-Tricks & cssportal.com— used for layout and responsive CSS reference


## PythonAnywhere Link

https://jpw14.pythonanywhere.com/