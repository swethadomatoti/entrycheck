# create_superuser.py
import os
import django
from django.contrib.auth import get_user_model

# Configure Django settings for standalone script
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entrycheck.settings")
django.setup()

User = get_user_model()

# Get values from Render environment variables
username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

# Only create if user doesn't already exist
if username and not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print(" Superuser already exists or environment variables not set.")
