from catalog.models import Brand, Category


def nav_categories(request):
    """Inject the category tree AND brands into every template.

    A context processor runs on every request and adds its returned dict to the
    template context — so the navbar/footer (which live in base.html and show on
    all pages) always have this data without each view passing it manually.

    - nav_categories: the FULL queryset of active categories (every level), not
      just roots. The {% recursetree %} tag in the navbar needs all nodes to walk
      the whole tree; it caches children internally, so this stays one query.
    - nav_brands: active brands (flat list) for the dynamic footer brand list.
    """
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    return {
        "nav_categories": categories,
        "nav_brands": brands,
    }
