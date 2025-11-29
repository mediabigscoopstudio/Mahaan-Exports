from django.contrib import admin
from .models import Enquiry,Category,Product,Article
from django.utils.html import format_html

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Enquiry Details', {
            'fields': ('full_name', 'email', 'phone_number', 'message')
        }),
        ('Meta Information', {
            'fields': ('created_at',),
        }),
    )

# -----------------------------
# CATEGORY ADMIN
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_on")
    list_filter = ("status", "created_on")
    search_fields = ("title", "meta_title", "meta_description")
    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("created_on",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "status")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords")
        }),
        ("Content", {
            "fields": ("content",)
        }),
        ("Meta", {
            "fields": ("created_on",)
        }),
    )


# -----------------------------
# PRODUCT ADMIN
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ("title", "category", "status", "created_on", "thumbnail_preview")
    list_filter = ("category", "status", "created_on")
    search_fields = ("title", "meta_title", "meta_description", "category__title")
    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("thumbnail_preview")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "category", "slug", "status")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords")
        }),
        ("Specifications", {
            "fields": (
                ("spec1heading", "spec1answer"),
                ("spec2heading", "spec2answer"),
                ("spec3heading", "spec3answer"),
                ("spec4heading", "spec4answer"),
                ("spec5heading", "spec5answer"),
            )
        }),
        ("Thumbnail", {
            "fields": ("thumbnail", "thumbnail_preview")
        }),
        ("Content", {
            "fields": ("content",)
        }),
        ("Meta", {
            "fields": ("created_on",)
        }),
    )

    # Thumbnail preview in admin
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width:80px; height:80px; object-fit:cover; border-radius:8px;" />',
                obj.thumbnail.url
            )
        return "No Image"
    
    thumbnail_preview.short_description = "Thumbnail"


# -----------------------------
# ARTICLE ADMIN
# -----------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ("title", "status", "created_on", "thumbnail_preview")
    list_filter = ("status", "created_on")
    search_fields = ("title", "meta_title", "meta_description")
    prepopulated_fields = {"slug": ("title",)}

    readonly_fields = ("created_on", "thumbnail_preview")

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "slug", "status")
        }),
        ("SEO", {
            "fields": ("meta_title", "meta_description", "meta_keywords")
        }),
        ("Thumbnail", {
            "fields": ("thumbnail", "thumbnail_preview")
        }),
        ("Content", {
            "fields": ("content",)
        }),
        ("Meta", {
            "fields": ("created_on",)
        }),
    )

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width:80px; height:80px; object-fit:cover; border-radius:8px;" />',
                obj.thumbnail.url
            )
        return "No Image"

    thumbnail_preview.short_description = "Thumbnail"