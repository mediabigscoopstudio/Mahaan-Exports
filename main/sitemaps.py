from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from dash.models import Product, Article

# ---- STATIC PAGES ----
class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "monthly"

    def items(self):
        return [
            'index',
            'about',
            'products',
            'articles',
            'contact',
            'privacy',
            'terms',
        ]

    def location(self, item):
        return reverse(item)


# ---- PRODUCTS ----
class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_on


# ---- ARTICLES ----
class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_on

