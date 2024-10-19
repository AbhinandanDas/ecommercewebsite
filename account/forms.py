from django import forms 
from .models import Customer,Address
from django.contrib.auth.forms import (AuthenticationForm,PasswordResetForm,SetPasswordForm)

class UserAddressForm(forms.ModelForm): 
    class Meta: 
        model = Address
        fields = ["full_name","phone","address_line","address_line2","town_city","postcode"]
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )

class UserLoginForm(AuthenticationForm): 
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'Username','id':'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'login-pwd'}))
    

class RegistrationForm(forms.ModelForm): 
    user_name = forms.CharField(label='Enter Username', min_length=5,max_length=50,help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta: 
        model = Customer
        fields = ('user_name','email')
    
    #Username already taken
    def clean_username(self): 
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)

        if r.count(): #r.count() will be greater than 0 if matches are found.
             raise forms.ValidationError('Username already taken.')
        return user_name
    
    #"Re enter the password" and "password" fields should match. 
    def clean_password2(self): 
        cd = self.cleaned_data
        if cd['password'] != cd['password2']: 
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']
    
    #Email already taken
    def clean_email(self): 
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists(): 
            raise forms.ValidationError('Email already exists, please use a different email of registration.')
        return email
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {
                'class' : 'form-control mb-3', 'placeholder': 'Username'
            }
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})

#Update the user details. 
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label='Account Email cannot be changed',max_length=200,widget=forms.TextInput(attrs={
        'class':'form-control mb-3',
        'placeholder':'email',
        'id':'form-email',
        'readonly':'readonly'
    }))

    # user_name = forms.CharField(label='Firstname',min_length=4,max_length=50,widget=forms.TextInput(attrs={
    #     'class':'form-control mb-3',
    #     'placeholder':'username',
    #     'id':'form-firstname',
    #     'readonly':'readonly'
    # }))
    first_name = forms.CharField(label='first name',min_length=4,max_length=50,widget=forms.TextInput(attrs={
        'class':'form-control mb-3',
        'placeholder':'firstname',
        'id':'form-fistname'
    }))

    class Meta: 
        model = Customer
        fields = ('email','first_name',)

    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        self.fields['first_name'].required=True
        self.fields['email'].required=True

class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs={
        'class':'form-control mb-3',
        'placeholder':'Email',
        'id':'form-email'
        }))
    def clean_data(self): 
        email = self.cleaned_data['email']
        u = Customer.objects.get(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunately we can not find that email address')
        return email    

class PwdResetConfirmForm(SetPasswordForm): 
    new_password1 = forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={
        'class':'form-control mb-3',
        'placeholder': 'Enter Password',
        'id': 'form-newpass'
    }))
    new_password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput(attrs={
            'class':'form-control mb-3',
            'placeholder': 'Repeat Password',
            'id': 'form-newpass2'
        }))
