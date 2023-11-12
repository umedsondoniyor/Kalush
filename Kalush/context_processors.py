from Product.models import Product, Category
from Profile.models import Profile


def default(request):
    categories = Category.objects.all()
    return {
        'categories': categories,
    }


