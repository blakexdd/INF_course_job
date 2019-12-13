from django import forms


# login form to login into account
class Loginform(forms.Form):
    # username field of user
    username = forms.CharField(max_length= 25,label="Enter username")

    # password field of user
    password = forms.CharField(max_length= 30, label='Password', widget=forms.PasswordInput)
