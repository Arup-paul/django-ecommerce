from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from catalog.models import Brand, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """Admin for the Category tree.

    DraggableMPTTAdmin (from mptt) renders categories as an indented,
    drag-and-drop tree instead of a flat list, so you can see and reorder the
    hierarchy visually. The first column showing the tree is added by mptt.
    """

    # Columns after mptt's tree column. 'indented_title' is mptt's helper that
    # draws the node name with indentation matching its depth in the tree.
    list_display = ("tree_actions", "indented_title", "slug", "is_active")
    # Make the indented title the clickable link to the edit page (not the
    # drag handle), so clicking a category name opens it.
    list_display_links = ("indented_title",)
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    # Auto-fill the slug field in the admin form as you type the name (JS).
    prepopulated_fields = {"slug": ("name",)}
    # Edit the active flag straight from the list view without opening each row.
    list_editable = ("is_active",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin for the flat Brand model — an ordinary list, no tree."""

    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("is_active",)
