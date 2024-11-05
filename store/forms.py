from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from .models import Profile

#updating User information
class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone'}),required=False)
    address1 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}),required=False)
    address2 = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}),required=False)
    city =  forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}),required=False)
    state = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}),required=False)
    zipcode = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'ZipCode'}),required=False)
    country = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}),required=False)
    
    class Meta:
        model = Profile
        fields = ('phone','address1','address2','city','state','zipcode','country')
        
#Creating a Password Change Form for updating user password here
class UpdatePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1','new_password2']
    def __init(self,*args,**kwargs):
        super(UpdatePasswordForm,self).__init__(*args,**kwargs)
        
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter Your Password'
        self.fields['new_password1'].label =""
        self.fields['new_password1'].help_text=  '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label =""
        self.fields['new_password2'].help_text= '<span class="form-text text-muted"><small>Enter Same password as above for verification.</small></span>'
        
#Creating a Update profile form UserChangeForm - doesnt allow password change we need diff class
class UpdateUserForm(UserChangeForm):
    #Hide password summary of built in UserChangeForm
    password = None 
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}),required=False)
    firstname = forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),required=False)
    lastname =forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),required=False)
    
    class Meta:
        model = User
        fields =('username','firstname','lastname','email')
        
    def __init(self,*args,**kwargs):
        super(UpdateUserForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        

#Signup page or login page form using UserCreationForm model
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}),required=False)
    firstname = forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter First Name'}),required=False)
    lastname =forms.CharField(label="",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Last Name'}),required=False)
    
    class Meta:
        model = User
        fields =('username','firstname','lastname','email','password1','password2')
    def __init(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Your Password'
        self.fields['password1'].label =""
        self.fields['password1'].help_text=  '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label =""
        self.fields['password2'].help_text= '<span class="form-text text-muted"><small>Enter Same password as above for verification.</small></span>'
        