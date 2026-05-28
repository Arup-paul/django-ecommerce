from django.shortcuts import render


def home_view(request):
    context = {
        'categories': [
            {'name': 'Electronics', 'icon': 'bi-laptop'},
            {'name': 'Fashion',     'icon': 'bi-bag'},
            {'name': 'Home',        'icon': 'bi-house-door'},
            {'name': 'Beauty',      'icon': 'bi-flower1'},
            {'name': 'Sports',      'icon': 'bi-bicycle'},
            {'name': 'Books',       'icon': 'bi-book'},
        ],
        'featured_products': [
            {'name': f'Sample Product {i}', 'old_price': 1499, 'new_price': 999}
            for i in range(1, 5)
        ],
    }
    return render(request, 'home.html', context)
