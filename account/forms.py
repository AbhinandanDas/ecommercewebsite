from django import forms 
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm

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
        model = UserBase
        fields = ('user_name','email')
    
    #Username already taken
    def clean_username(self): 
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)

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
        if UserBase.objects.filter(email=email).exists(): 
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
