from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import UserRole

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up initial data for the restaurant dashboard'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create default roles if they don't exist
        roles = {
            'leadership': 'SB Leadership Team',
            'country_leadership': 'Country Leadership Team',
            'country_admin': 'Country Admin Team',
            'branch_manager': 'Branch Manager',
        }
        
        for role_name, description in roles.items():
            role, created = UserRole.objects.get_or_create(
                name=role_name,
                defaults={'description': description}
            )
            
            if created:
                self.stdout.write(f'Created role: {role_name}')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role=UserRole.objects.get(name='leadership')
            )
            self.stdout.write('Created superuser: admin@example.com')
        
        self.stdout.write(self.style.SUCCESS('Initial data setup complete!'))
