import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey


@deconstructible
class UploadTo:
    """Reusable upload_to for image fields, written once for every model.

    Drops the user's original filename (privacy + unsafe chars) and stores a
    UUID name, keeping only the extension — e.g. UploadTo("brands") yields
    paths like "brands/<uuid>.jpg".

    It's a @deconstructible class (not a closure) because Django must be able
    to serialize the upload_to value into migration files by reconstructing it
    as `UploadTo("brands")`. A nested function can't be referenced that way.
    """

    def __init__(self, folder):
        self.folder = folder

    def __call__(self, instance, filename):
        ext = os.path.splitext(filename)[1].lower()
        return f"{self.folder}/{uuid.uuid4().hex}{ext}"


class Category(MPTTModel):
    """A product category in a tree (e.g. Electronics > Phones > Smartphones).

    Subclasses MPTTModel instead of models.Model so django-mptt can add and
    maintain the tree bookkeeping columns (lft, rght, tree_id, level) for us.
    Those let us fetch a whole branch in one fast query instead of recursing.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("name"), max_length=150)
    # slug = the URL-safe version of the name (e.g. "Feature Phones" -> "feature-phones").
    # Used in category URLs. Unique so each category has one canonical address.
    slug = models.SlugField(_("slug"), max_length=160, unique=True, blank=True)

    # The parent category. TreeForeignKey is mptt's FK that renders as an
    # indented tree dropdown in forms/admin. A NULL parent = a root (top-level)
    # category. related_name="children" lets us write `category.children.all()`.
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("parent category"),
    )

    description = models.TextField(_("description"), blank=True)
    image = models.ImageField(
        _("image"), upload_to=UploadTo("categories"), blank=True, null=True
    )
    # Soft on/off switch — hide a category from the storefront without deleting it.
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        # mptt-specific Meta: order siblings (same parent) by name in the tree.
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate the slug from the name if one wasn't provided.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """A product brand/manufacturer (e.g. Apple, Samsung, Nike).

    A plain flat model (subclasses models.Model, not MPTTModel) — brands have
    no hierarchy, so there's no parent/tree here. Contrast with Category above.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_("name"), max_length=150, unique=True)
    slug = models.SlugField(_("slug"), max_length=160, unique=True, blank=True)

    description = models.TextField(_("description"), blank=True)
    logo = models.ImageField(
        _("logo"), upload_to=UploadTo("brands"), blank=True, null=True
    )
    # Soft on/off switch — hide a brand from the storefront without deleting it.
    is_active = models.BooleanField(_("active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")
        # Brands have no tree, so we sort the flat list alphabetically by name.
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate the slug from the name if one wasn't provided.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
