from django.contrib import admin
from django.urls import path
from dash import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
handler400 = views.custom_400
handler403 = views.custom_403
handler404 = views.custom_404
handler500 = views.custom_500

urlpatterns = [
    path("",views.index,name='index'),
    path("admin/", admin.site.urls),
    path("login_view",views.login_view,name='login_view'),
    path("logout_view",views.logout_view,name='logout_view'),

    path("articles",views.articles,name='articles'),
    path("add_article",views.add_article,name='add_article'),
    path("edit_article/<slug>",views.edit_article,name='edit_article'),
    path("enable_article/<int:id>",views.enable_article,name='enable_article'),
    path("disable_article/<int:id>",views.disable_article,name='disable_article'),
    path("delete_article/<int:id>",views.delete_article,name='delete_article'),

    path("categories",views.categories,name='categories'),
    path("add_category",views.add_category,name='add_category'),
    path("edit_category/<slug>",views.edit_category,name='edit_category'),
    path("delete_category/<int:id>",views.delete_category,name='delete_category'),
    path("enable_category/<int:id>",views.enable_category,name='enable_category'),
    path("disable_category/<int:id>",views.disable_category,name='disable_category'),

    path("products",views.products,name='products'),
    path("add_product",views.add_product,name='add_product'),
    path("edit_product/<slug>",views.edit_product,name='edit_product'),
    path("delete_product/<int:id>",views.delete_product,name='delete_product'),
    path("enable_product/<int:id>",views.enable_product,name='enable_product'),
    path("disable_product/<int:id>",views.disable_product,name='disable_product'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)