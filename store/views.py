from django.shortcuts import get_object_or_404, render

from .models import Category, Product


# Home Page
def products_all(request):
    products = Product.products.all() # select * from products;
    return render(request,'store/home.html',{'products':products})

#product detail page for single item
def product_detail(request,slug): # slug = fade
    product = get_object_or_404(Product, slug=slug,in_stock=True) # select * from product where slug = "fade" and in_stock=True;
    return render(request,'store/products/single.html',{'product':product})

#category list page for products falling under requested category name
def category_list(request,category_slug): # select * from category where category_slug = 'django'
    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(categories=category)
    return render(request,'store/products/category.html',{'category':category,'products':products})

