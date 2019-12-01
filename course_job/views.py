from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, render_to_response
from django.contrib.auth import login, logout, get_user_model
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
import os
from organizations.views import Organization
from django.template import RequestContext

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


# openning json file to read info from it
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

def org_page(request):
    return render(request, 'griddynamics.html', {})

# view function for home page
def home(request):
    # assigning organizations to organizations variable
    organizations = list(Organization.objects.all())

    # creating list there each row
    # consists of three organizations
    list_of_three = []
    empty_org =  dict(id = -1, name = 0)

    # if amount of organizations that is not
    # dividable by 3, we assign zeroes to make
    # len of out list divided by 3
    if len(organizations) % 3 == 2:
        organizations.append(empty_org)
    elif len(organizations) % 3 == 1:
        organizations.append(empty_org)
        organizations.append(empty_org)

    # filling in list_of_three list
    for i in range(0, len(organizations), 3):
        list_of_three.append([organizations[i], organizations[i + 1], organizations[i + 2]])

    # creating dict to give it
    # as third parameter to
    # render function
    vars = dict(organizations=list_of_three)

    return render(request, 'index.html', vars)