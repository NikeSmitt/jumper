from mainapp.models.category import Category


def get_categories(request):
    return {
        'categories': Category.objects.filter(parent__isnull=True),
        # 'spam': Category.objects.all()[:5],
    }
