from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Brand, Category

# A nested dict describing the category tree. Each key is a category name; its
# value is a dict of children (empty dict = leaf node). Keeping the data here
# (separate from the logic below) makes the tree easy to read and edit.
CATEGORY_TREE = {
    "Electronics": {
        "Phones": {
            "Smartphones": {},
            "Feature Phones": {},
        },
        "Laptops": {
            "Gaming Laptops": {},
            "Ultrabooks": {},
        },
        "Accessories": {},
    },
    "Clothing": {
        "Men": {
            "Shirts": {},
            "Trousers": {},
        },
        "Women": {
            "Dresses": {},
            "Tops": {},
        },
    },
    "Home & Kitchen": {
        "Furniture": {},
        "Cookware": {},
    },
}

BRANDS = ["Apple", "Samsung", "Sony", "Nike", "Adidas", "Dell", "HP", "IKEA"]


class Command(BaseCommand):
    # Shown when you run `manage.py help seed_catalog`.
    help = "Seed sample categories (as an MPTT tree) and brands. Safe to re-run."

    def handle(self, *args, **options):
        # Wrap everything in one transaction: if any insert fails, the whole
        # seed rolls back so we never end up with a half-built tree.
        with transaction.atomic():
            self._seed_categories()
            self._seed_brands()
        self.stdout.write(self.style.SUCCESS("Catalog seed complete."))

    def _seed_categories(self):
        # Recursively walk CATEGORY_TREE, creating each node under its parent.
        def create_nodes(subtree, parent=None):
            for name, children in subtree.items():
                # get_or_create makes this idempotent: re-running won't create
                # duplicates, it just fetches the existing row. The model's
                # save() fills in the slug, so we don't pass one here.
                category, created = Category.objects.get_or_create(
                    name=name, parent=parent
                )
                verb = "Created" if created else "Exists "
                self.stdout.write(f"  [{verb}] category: {category}")
                # Recurse into this node's children, passing it as their parent.
                create_nodes(children, parent=category)

        self.stdout.write(self.style.MIGRATE_HEADING("Seeding categories..."))
        create_nodes(CATEGORY_TREE)

    def _seed_brands(self):
        self.stdout.write(self.style.MIGRATE_HEADING("Seeding brands..."))
        for name in BRANDS:
            brand, created = Brand.objects.get_or_create(name=name)
            verb = "Created" if created else "Exists "
            self.stdout.write(f"  [{verb}] brand: {brand}")
