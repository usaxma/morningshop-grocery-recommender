from django import forms
from .models import * 
class userForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        
        # fields = (Email, Password, FirstName,LastName, Gender, DateOfBirth, Phone, Address,  City ,Country ,zipCode)
        # labels = {
        #     'FirstName':'First Name',
        #     'Last Name':'Last Name',
        #     'DateOfBirth':'D-O-B',
        #     'zipCode':'ZIP-CODE',
        #     'password':'Password',
        #     'password2':'RePassword',
        #     'address':'Address',
        #     'dob':'D-O-B',
        #     'gender':'Gender',}


#         fields = '__all__'

    