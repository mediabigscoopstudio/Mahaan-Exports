from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.template.loader import render_to_string
from dash.models import Enquiry,Article,Product,Category
def index(request):
     stuff = Product.objects.all()[:4]
     return render(request,'main/index.html',{'stuff':stuff})

def robots_txt(request):
    content = render_to_string("main/robots.txt")
    return HttpResponse(content, content_type="text/plain")

def about(request):
     return render(request,'main/about.html')

def contact(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        Enquiry.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone,
            message=message
        )
        return redirect('/thank_you')  # or a success page

    return render(request, "main/contact.html")

def enq_form(request):
     if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        category = request.POST.get('category')

        Enquiry.objects.create(
            full_name=full_name,
            email=email,
            phone_number=phone,
            message=message,
            category=category,
        )
     return redirect('/thank_you')

def thank_you(request):
     return render(request,'main/thank_you.html')

def privacy(request):
     return render(request,'main/privacy.html')

def terms(request):
     return render(request,'main/terms.html')

def product(request,slug):
     data = get_object_or_404(Product,slug=slug)
     others = Product.objects.order_by('-created_on')[:3]
     context={
          'data':data,
          'others':others
     }
     return render(request,'main/products/product.html',context)

def products(request):
    categories = Category.objects.filter(status='active')
    products = Product.objects.all().order_by("created_on")

    return render(request, "main/products/products.html", {
        "categories": categories,
        "products": products,
    })
def articles(request):
     articles = Article.objects.order_by('-created_on')
     return render(request,'main/articles/articles.html',{'articles':articles})

def article(request,slug):
     data = get_object_or_404(Article,slug=slug)
     others = Article.objects.all()[:3]
     context = {
          'data':data,
          'others':others
     }
     return render(request,'main/articles/article.html',context)