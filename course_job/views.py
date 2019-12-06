from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
import json
from organizations.views import Organization
from .forms import Loginform

# assigning organizations to organizations variable
organizations = list(Organization.objects.all())

# creating list there each row
# consists of three organizations
list_of_three = []
empty_org = dict(id=-1, name=0)

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


# view function for start page
def index(request):
    return render(request, 'index.html', dict_index)


# view function for logout page
def page_logout(request):
    logout(request)

    return HttpResponseRedirect('/')


# view function for login page
def page_login(request):
    # initializing username and password values
    uservalue = ''
    passwordvalue = ''

    # creating login form and assigning it to form variable
    form = Loginform(request.POST or None)

    # checking if form is valid and if yes
    # getting username and password of user
    # then auntificate user and redirect to main page
    if form.is_valid():
        # assigning username and password variables
        uservalue = form.cleaned_data.get('username')
        passwordvalue = form.cleaned_data.get('password')

        # auntificating user
        user = authenticate(username=uservalue, password=passwordvalue)

        # if user exists redirect to main page
        # else print error
        if user is not None:
            login(request, user)
            context = {'form': form,
                       'error': 'The login has been successful',
                       'organizations': list_of_three}

            return render(request, 'index.html', context)
        else:
            context = {'form': form,
                       'error': 'The username and password combination is incorrect'}

            return render(request, 'login.html', context)
    else:
        context = {'form': form}
        return render(request, 'login.html', context)


# view function for home page
def home(request):

    # creating dict to give it
    # as third parameter to
    # render function
    vars = dict(organizations=list_of_three)

    return render(request, 'index.html', vars)