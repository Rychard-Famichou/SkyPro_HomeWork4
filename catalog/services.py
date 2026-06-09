from .models import Product


class CatalogService:
    @staticmethod
    def get_category_products(category_id):
        products = Product.objects.filter(category_id=category_id)
        return products
