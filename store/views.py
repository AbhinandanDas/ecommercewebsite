from django.shortcuts import get_object_or_404, render

from review.models import Review

from .models import Category, Product, ProductImage


# Home Page
def products_all(request):
    products = Product.objects.prefetch_related("product_image").filter(is_active=True)  # select * from products;
    return render(
        request,
        "store/index.html",
        {"products": products},
    )


# product detail page for single item
def product_detail(request, slug):  # slug = fade
    product = get_object_or_404(
        Product, slug=slug, is_active=True
    )  # select * from product where slug = "fade" and in_stock=True;
    reviews = Review.objects.filter(
        product=product
    )  # select * from review where product = product
    return render(
        request,
        "store/single.html",
        {"product": product, "reviews": reviews, "range": range(1, 6)},
    )


# category list page for products falling under requested category name
def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {'category': category, 'products': products})
    # category = get_object_or_404(Category, slug=category_slug)
    # products = Product.objects.filter(
    #     category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    # )
    # return render(request, "store/category.html", {"category": category, "products": products})
