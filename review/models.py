from django.db import models
from django.conf import settings
from store.models import Product

class ReviewManager(models.Manager): 
    def get_queryset(self):
        return super(ReviewManager,self).get_queryset().filter(is_spam=False)

# Create your models here.
class Review(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_review')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_review')
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    rating = models.PositiveIntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False)
    objects = models.Manager()
    reviews = ReviewManager()

    class Meta: 
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.title)
