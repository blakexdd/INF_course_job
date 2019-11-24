from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.contrib.auth import login, logout, get_user_model
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import os

# creating register form class
class RegisterFormView(FormView):
    form_class = UserCreationForm

    # redirecting link
    success_url = "/login/"

    # template page
    template_name = "register.html"

    def form_valid(self, form):
        # save user if data is correct
        form.save()

        # return base class method
        return super(RegisterFormView, self).form_valid(form)

# login to account class
class LoginFormView(FormView):
    form_class = AuthenticationForm

    template_name = 'login.html'

    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)

# exit class
class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect('/')

@login_required
def userdashboardview(request):
    render(request, 'personal_cab.html',
           {'userfileslist': os.listdir(get_user_model().username)})


#openning json file to read info from it
with open('package.json', 'r') as read_file:
    # load data from json file to data variable
    data = json.load(read_file)

    # assigning data from data to organizations variable
    organizations = data['organizations']

    # forming dictionary of parameters to give
    # it as a third argument to render function
    # for index page
    dict_index = {'organizations': organizations}



def index(request):
    return render(request, 'index.html', dict_index)