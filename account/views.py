from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,render
from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase
from django.template.loader import render_to_string
from .forms import RegistrationForm,UserEditForm
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .models import UserBase
from .token import account_activation_token

# Create your views here.

@login_required
def dashboard(request): 
    return render(request,'account/user/dashboard.html')


@login_required
def user_logout(request): 
    logout(request)
    return render(request,'account/registration/logout.html')

@login_required
def edit_details(request): 
    if request.method == 'POST': 
        user_form = UserEditForm(instance=request.user,data=request.POST)

        if user_form.is_valid(): 
            user_form.save()
    else: 
        user_form = UserEditForm(instance=request.user)

    return render(request,'account/user/edit_details.html',{'user_form': user_form})    

@login_required
def delete_user(request): 
    user = UserBase.objects.get(user_name=request.user)
    user.is_active=False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

def account_register(request): 
    #check if user is logged in. 
    if request.user.is_authenticated: 
        return redirect('account:dashboard')
    
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
            user.email_user(subject=subject, message=message)
            return HttpResponse('Registered successfully and activation link has been sent to email.')
    #display the registration page/signup page.     
    else: 
        registerForm = RegistrationForm()
    return render(request,'account/registration/register.html', {'form':registerForm})    


def account_activate(request,uidb64,token): 
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        #check if uid is present in database.
        user = UserBase.objects.get(pk=uid)
    except(TypeError,ValueError, OverflowError, user.DoesNotExist): 
        user = None
    if user is not None and account_activation_token.check_token(user,token): 
        user.is_active=True
        user.save()
        login(request,user)
        return redirect('account:dashboard')
    else: 
        return render('account/registration/activation_invalid.html')