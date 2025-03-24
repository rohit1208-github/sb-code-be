## Create a superuser and attach leadership role to the user.

First create the superuser.
```python
python manage.py createsuperuser
```

Then make sure you replace the sbadmin@sb.com to your user.
```python
from users.models import UserRole, User

# Create or get the leadership role
leadership_role, created = UserRole.objects.get_or_create(
    name=UserRole.LEADERSHIP,
    defaults={'description': 'SB Leadership Team'}
)

if created:
    print("Leadership role created.")
else:
    print("Leadership role already exists.")

# Get the superuser and attach the leadership role
try:
    user = User.objects.get(email="sbadmin@sb.com")
    user.role = leadership_role
    user.save()
    print("Leadership role attached to the superuser.")
except User.DoesNotExist:
    print("Superuser with email 'sbadmin@sb.com' does not exist.")
```
