from django.core.management import BaseCommand, call_command

from blog.models import Post
from catalog.models import Category, Product
from users.models import CustomUser


class Command(BaseCommand):
    help = "Load test data from fixture to database"

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Category.objects.all().delete()
        Product.objects.all().delete()
        Post.objects.all().delete()
        CustomUser.objects.all().delete()

        call_command('loaddata', 'groups_fixture.json', natural_foreign=True)
        call_command('loaddata', 'users_fixture.json', natural_foreign=True)
        call_command('loaddata', 'categories_fixture.json')
        call_command('loaddata', 'products_fixture.json')
        call_command('loaddata', 'posts_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
