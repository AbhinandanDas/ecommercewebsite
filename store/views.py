from django.shortcuts import render,get_object_or_404

from .models import Category,Product


# Home Page
def products_all(request):
    products = Product.products.all() # select * from products;
    return render(request,'store/home.html',{'products':products})


def product_detail(request,slug):
    product = get_object_or_404(Product, slug=slug,in_stock=True) # select * from product where slug = "django" and in_stock=True;
    return render(request,'store/products/detail.html',{'product':product})

def category_list(request,category_slug): # select * from category where category_slug = 'django'
    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(categories=category)
    return render(request,'store/products/category.html',{'category':category,'products':products})

