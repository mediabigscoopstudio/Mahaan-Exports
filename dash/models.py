from django.db import models
from django.utils.text import slugify

class Enquiry(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"Enquiry from {self.full_name} ({self.email})"
    
class Category(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    title = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    content = models.TextField(blank=True, null=True)

    slug = models.SlugField(unique=True, max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Product(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products",blank=True, null=True)

    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    # Specifications
    spec1heading = models.CharField(max_length=255, blank=True, null=True)
    spec1answer = models.TextField(blank=True, null=True)

    spec2heading = models.CharField(max_length=255, blank=True, null=True)
    spec2answer = models.TextField(blank=True, null=True)

    spec3heading = models.CharField(max_length=255, blank=True, null=True)
    spec3answer = models.TextField(blank=True, null=True)

    spec4heading = models.CharField(max_length=255, blank=True, null=True)
    spec4answer = models.TextField(blank=True, null=True)

    spec5heading = models.CharField(max_length=255, blank=True, null=True)
    spec5answer = models.TextField(blank=True, null=True)

    thumbnail = models.ImageField(upload_to="products/", blank=True, null=True)

    content = models.TextField(blank=True, null=True)

    slug = models.SlugField(unique=True, max_length=255)

    created_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return f"/product/{self.slug}"

    def __str__(self):
        return self.title
    

class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.TextField(blank=True, null=True)

    thumbnail = models.ImageField(upload_to="articles/", blank=True, null=True)

    content = models.TextField()

    slug = models.SlugField(unique=True, max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return f"/article/{self.slug}"

    def __str__(self):
        return self.title
