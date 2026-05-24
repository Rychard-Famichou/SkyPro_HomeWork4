from django.core.management import BaseCommand, call_command

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Load test data from fixture to database"

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Category.objects.all().delete()
        Product.objects.all().delete()

        call_command('loaddata', 'categories_fixture.json')
        call_command('loaddata', 'products_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
        