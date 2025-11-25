from django.shortcuts import render,redirect,get_object_or_404
from .models import Enquiry,Article,Product,Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import uuid
from django.utils.text import slugify

def superadmin_required(user):
    return user.is_superuser 

def login_view(request):
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'dash/signin.html')

def logout_view(request):
    logout(request)
    return redirect('/login_view')

def custom_error_handler(request, status_code, exception=None):
    return render(request, 'dash/error.html', {'status_code': status_code, 'message': exception}, status=status_code)

def custom_404(request, exception):
    return custom_error_handler(request, 404, exception)

def custom_500(request):
    return custom_error_handler(request, 500)

def custom_403(request, exception):
    return custom_error_handler(request, 403, exception)

def custom_400(request, exception):
    return custom_error_handler(request, 400, exception)


@user_passes_test(superadmin_required, login_url='/login_view') 
def index(request):
    enqs = Enquiry.objects.all()
    stuff = Product.objects.all()[:4]
    context={
        'enqs':enqs,
        'stuff':stuff,
    }
    return render(request,'dash/index.html',context)

@user_passes_test(superadmin_required, login_url='/login_view') 
def articles(request):
    articles = Article.objects.order_by('-created_on')
    return render(request,'dash/articles/article.html',{'articles':articles})

def add_article(request):
    if request.method == "POST":

        title = request.POST.get("title")
        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")
        meta_keywords = request.POST.get("meta_keywords")
        content = request.POST.get("content")
        # File inputs
        thumbnail = request.FILES.get("thumbnail")

        # Generate unique slug
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Article.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Validate required fields
        if not title or not content or not thumbnail:
            messages.error(request, "Please fill all required fields.")
            return redirect("add_article")

        # Save article
        article = Article.objects.create(
            title=title,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            thumbnail=thumbnail,
            content=content,
        )

        messages.success(request, "Article created successfully!")
        return redirect("/articles", slug=article.slug)

    return render(request, "dash/articles/add_article.html")

def edit_article(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == "POST":

        title = request.POST.get("title")
        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")
        meta_keywords = request.POST.get("meta_keywords")
        content = request.POST.get("content")

        thumbnail = request.FILES.get("thumbnail")

        # Basic validation
        if not title or not content:
            messages.error(request, "Title and content are required.")
            return redirect("edit_article", slug=article.slug)

        # IF title changed → generate NEW unique slug
        if title != article.title:
            base_slug = slugify(title)
            new_slug = base_slug
            counter = 1

            while Article.objects.filter(slug=new_slug).exclude(id=article.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1

            article.slug = new_slug

        # Update fields
        article.title = title
        article.meta_title = meta_title
        article.meta_description = meta_description
        article.meta_keywords = meta_keywords
        article.content = content

        # If new thumbnail uploaded → replace
        if thumbnail:
            article.thumbnail = thumbnail

        article.save()

        messages.success(request, "Article updated successfully!")
        return redirect("/articles", slug=article.slug)

    return render(request, "dash/articles/edit_article.html", {
        "article": article
    })

def disable_article(request,id):
     data = get_object_or_404(Article,id=id)
     data.status = "draft"
     data.save()
     return redirect('/articles')

def enable_article(request,id):
     data = get_object_or_404(Article,id=id)
     data.status = "published"
     data.save()
     return redirect('/articles')

def delete_article(request,id):
     data = get_object_or_404(Article,id=id)
     data.delete()
     return redirect('/articles')

@user_passes_test(superadmin_required, login_url='/login_view') 
def categories(request):
    cats = Category.objects.all()
    return render(request,'dash/category/categories.html',{'cats':cats})

def add_category(request):
    if request.method == "POST":

        title = request.POST.get("title")
        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")
        meta_keywords = request.POST.get("meta_keywords")
        content = request.POST.get("content")

        if not title:
            messages.error(request, "Category title is required.")
            return redirect("add_category")

        # Generate unique slug automatically
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Category.objects.create(
            title=title,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            content=content,
            slug=slug,
        )

        messages.success(request, "Category created successfully!")
        return redirect("/categories")

    return render(request, "dash/category/add_category.html")

def edit_category(request, slug):

    category = get_object_or_404(Category, slug=slug)

    if request.method == "POST":

        title = request.POST.get("title")
        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")
        meta_keywords = request.POST.get("meta_keywords")
        content = request.POST.get("content")

        if not title:
            messages.error(request, "Title cannot be empty.")
            return redirect("edit_category", slug=category.slug)

        # Regenerate slug ONLY IF title changed
        if title != category.title:
            base_slug = slugify(title)
            new_slug = base_slug
            counter = 1
            while Category.objects.filter(slug=new_slug).exclude(id=category.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            category.slug = new_slug

        # Update fields
        category.title = title
        category.meta_title = meta_title
        category.meta_description = meta_description
        category.meta_keywords = meta_keywords
        category.content = content

        category.save()

        messages.success(request, "Category updated successfully!")
        return redirect("/categories")

    return render(request, "dash/category/edit_category.html", {
        "category": category
    })

def delete_category(request,id):
     data = get_object_or_404(Category,id=id)
     data.delete()
     return redirect('/categories')

def disable_category(request,id):
     data = get_object_or_404(Category,id=id)
     data.status = "inactive"
     data.save()
     return redirect('/categories')

def enable_category(request,id):
     data = get_object_or_404(Category,id=id)
     data.status = "active"
     data.save()
     return redirect('/categories')


@user_passes_test(superadmin_required, login_url='/login_view') 
def products(request):
    stuff = Product.objects.all()
    return render(request,'dash/products/products.html',{'stuff':stuff})

def add_product(request):

    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST.get("title")
        category_id = request.POST.get("category")
        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")
        meta_keywords = request.POST.get("meta_keywords")

        # Specs
        spec1heading = request.POST.get("spec1heading")
        spec1answer = request.POST.get("spec1answer")
        spec2heading = request.POST.get("spec2heading")
        spec2answer = request.POST.get("spec2answer")
        spec3heading = request.POST.get("spec3heading")
        spec3answer = request.POST.get("spec3answer")
        spec4heading = request.POST.get("spec4heading")
        spec4answer = request.POST.get("spec4answer")
        spec5heading = request.POST.get("spec5heading")
        spec5answer = request.POST.get("spec5answer")

        content = request.POST.get("content")

        thumbnail = request.FILES.get("thumbnail")

        if not title or not thumbnail or not content:
            messages.error(request, "Please fill all required fields.")
            return redirect("add_product")

        category = get_object_or_404(Category, id=category_id)

        # Auto slug
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Product.objects.create(
            title=title,
            category=category,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,

            spec1heading=spec1heading,
            spec1answer=spec1answer,
            spec2heading=spec2heading,
            spec2answer=spec2answer,
            spec3heading=spec3heading,
            spec3answer=spec3answer,
            spec4heading=spec4heading,
            spec4answer=spec4answer,
            spec5heading=spec5heading,
            spec5answer=spec5answer,

            thumbnail=thumbnail,
            content=content,
            slug=slug
        )

        messages.success(request, "Product created successfully!")
        return redirect("/products")

    return render(request, "dash/products/add_products.html", {
        "categories": categories
    })

def edit_product(request, slug):

    product = get_object_or_404(Product, slug=slug)
    categories = Category.objects.all()

    if request.method == "POST":

        title = request.POST.get("title")
        category_id = request.POST.get("category")

        meta_title = request.POST.get("meta_title")
        meta_description = request.POST.get("meta_description")
        meta_keywords = request.POST.get("meta_keywords")

        spec1heading = request.POST.get("spec1heading")
        spec1answer = request.POST.get("spec1answer")
        spec2heading = request.POST.get("spec2heading")
        spec2answer = request.POST.get("spec2answer")
        spec3heading = request.POST.get("spec3heading")
        spec3answer = request.POST.get("spec3answer")
        spec4heading = request.POST.get("spec4heading")
        spec4answer = request.POST.get("spec4answer")
        spec5heading = request.POST.get("spec5heading")
        spec5answer = request.POST.get("spec5answer")

        content = request.POST.get("content")
        thumbnail = request.FILES.get("thumbnail")

        if not title or not content:
            messages.error(request, "Title and content cannot be empty.")
            return redirect("edit_product", slug=product.slug)

        category = get_object_or_404(Category, id=category_id)

        # If title changed → new slug
        if title != product.title:
            base_slug = slugify(title)
            new_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=new_slug).exclude(id=product.id).exists():
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = new_slug

        # Update fields
        product.title = title
        product.category = category
        product.meta_title = meta_title
        product.meta_description = meta_description
        product.meta_keywords = meta_keywords

        product.spec1heading = spec1heading
        product.spec1answer = spec1answer
        product.spec2heading = spec2heading
        product.spec2answer = spec2answer
        product.spec3heading = spec3heading
        product.spec3answer = spec3answer
        product.spec4heading = spec4heading
        product.spec4answer = spec4answer
        product.spec5heading = spec5heading
        product.spec5answer = spec5answer

        product.content = content

        if thumbnail:
            product.thumbnail = thumbnail

        product.save()

        messages.success(request, "Product updated successfully!")
        return redirect("/products")

    return render(request, "dash/products/edit_products.html", {
        "product": product,
        "categories": categories
    })



def delete_product(request,id):
     data = get_object_or_404(Product,id=id)
     data.delete()
     return redirect('/products')

def disable_product(request,id):
     data = get_object_or_404(Product,id=id)
     data.status = "inactive"
     data.save()
     return redirect('/products')

def enable_product(request,id):
     data = get_object_or_404(Product,id=id)
     data.status = "active"
     data.save()
     return redirect('/products')