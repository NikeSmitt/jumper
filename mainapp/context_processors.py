from mainapp.forms import ProductSearchForm
from mainapp.models.category import Category


def get_categories(request):
    return {
        'categories': Category.objects.filter(parent__isnull=True, header_show=True),
        'form': ProductSearchForm(),
        'banner_cat': Category.objects.filter(slug__in=['man', 'woman', 'basketball']),
    }
