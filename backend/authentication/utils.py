from django.contrib.auth import get_user_model

User = get_user_model()


def create_superuser():
    email = 'egyahmed.ezzat120@gmail.com'
    if User.objects.filter(email=email).exists():
        return
    
    User.objects.create_superuser(
        email,
        'admin',
        'admin',
    )
    print('[+] Superuser created successfully.')
