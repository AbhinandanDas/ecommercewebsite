from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

#Post the reviews and persist into our model. 
@login_required
def add_review(request): 
    pass 
