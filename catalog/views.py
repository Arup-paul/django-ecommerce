from django.shortcuts import render

from catalog.models import Category


def category_list(request):
    """Storefront page showing the full category tree.

    Passes the FULL queryset of active categories (every level) so the template
    can render it with mptt's {% recursetree %} tag — same data shape the navbar
    uses. The navbar's nav_categories comes from the context processor; this
    view passes its own `categories` so the page works even if that changes.
    """
    categories = Category.objects.filter(is_active=True)
    return render(request, "catalog/category_list.html", {"categories": categories})
