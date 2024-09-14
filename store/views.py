from django.shortcuts import get_object_or_404, render
from review.models import Review
from .models import Category, Product



# Home Page
def products_all(request):
    products = Product.products.all() # select * from products;
    return render(request,'store/index.html',{'products':products})

#product detail page for single item
def product_detail(request,slug): # slug = fade
    product = get_object_or_404(Product, slug=slug,in_stock=True) # select * from product where slug = "fade" and in_stock=True;
    reviews = Review.objects.filter(product=product)# select * from review where product = product
    return render(request,'store/single.html',{'product':product, 'reviews':reviews, 'range':range(1,6)})

#category list page for products falling under requested category name
def category_list(request,category_slug): # select * from category where category_slug = 'django'
    category = get_object_or_404(Category,slug=category_slug)
    products = Product.objects.filter(categories=category)
    return render(request,'store/category.html',{'category':category,'products':products})

