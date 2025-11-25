from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import StaticViewSitemap, ProductSitemap, ArticleSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "products": ProductSitemap,
    "articles": ArticleSitemap,
}
urlpatterns = [
    path("",views.index,name='index'),
    path("about",views.about,name='about'),
    path("contact",views.contact,name='contact'),
    path("thank_you",views.thank_you,name='thank_you'),
    path("privacy",views.privacy,name='privacy'),
    path("terms",views.terms,name='terms'),

    path("products",views.products,name='products'),
    path("product/<slug>",views.product,name='product'),

    path("articles",views.articles,name='articles'),
    path("article/<slug>",views.article,name='article'),

    path("enq_form",views.enq_form,name='enq_form'),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django_sitemap"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)