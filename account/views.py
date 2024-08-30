from django.shortcuts import redirect,render
from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase
from django.template.loader import render_to_string
from .forms import RegistrationForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import UserBase
from .token import account_activation_token

# Create your views here.

def account_register(request): 
    #check if user is logged in. 
    if request.user.is_authenticated: 
        return redirect('/')
    
    if request.method == 'POST': 
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid(): 
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password = registerForm.cleaned_data['password']
            user.is_active = False #Set this to true after email verification. 
            user.save()

            #setup email 
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user' : user,
                'domain' : current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : account_activation_token.make_token(user)
            })
