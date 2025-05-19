from django.contrib.auth import get_user_model
from django.db import IntegrityError

def create_super():
    User = get_user_model()
    username = "admin"
    email = "admin@django.com"
    password = "Aigerim2006"

    if not User.objects.filter(username=username).exists():
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            print("✅ Superuser created.")
        except IntegrityError:
            print("⚠️ Superuser creation failed due to integrity error.")
    else:
        print("ℹ️ Superuser already exists.")
