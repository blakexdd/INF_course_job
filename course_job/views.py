from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
import json
from organizations.views import Organization
from .forms import Loginform
from organizations.forms import Editing_Organization, Editing_Person, Editing_Days
from organizations.views import updating_organizations

# creating list there each row
# consists of three organizations
list_of_three = []

# creating dict_index
dict_index = {}

def update_list_of_three():
    # assigning organizations to organizations variable
    organizations = list(Organization.objects.all())

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

update_list_of_three()


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

# view function for editing organizations
def create_organizations(request):
    # creating form
    organization_form = Editing_Organization(request.POST or None)
    # initializing error variable
    error = ""

    # checking if form is valid
    if organization_form.is_valid():
        # getting information about organization
        organization_name = organization_form.cleaned_data.get('name')
        organization_year_of_est = organization_form.cleaned_data.get('year_of_est')
        organization_location = organization_form.cleaned_data.get('location')
        organization_new_location = organization_location.split(',')
        organziation_index = organization_new_location[0]
        organization_city = organization_new_location[1]
        organization_adress = organization_new_location[2]
        organization_brief_description = organization_form.cleaned_data.get('brief_description')

        # forming organization dictionary
        new_organization = dict(name=organization_name,
                                year_of_establishing=organization_year_of_est,
                                location=dict(index=organziation_index,
                                              city=organization_city,
                                              adress=organization_adress),
                                brief_decription=organization_brief_description)

        # opening json file to add there information about new organization
        with open('package.json', 'r') as read_file:
            # load data from json file to data variable
            data = json.load(read_file)

            # assigning data from data to organizations variable
            organizations = data['organizations']

            # initializing flag if organization exists
            flag = 0

            # going through organizations and finding created organization in list
            for i in range(len(organizations)):
                if organizations[i]['name'] == organization_name:
                    flag = i

            if flag == 0:
                organizations.append(new_organization)
            else:
                error = 'Organization already exists'

        #forming dictionary to load in json
        org = dict(organizations=organizations)

        # oppening json file and adding information to it
        with open('package.json', 'w') as write_file:
            json.dump(org, write_file)
            #print('Organization[-1]:', organizations[-1])

            #print('==================================')
            #print(organizations)

        #print(new_organization)

        updating_organizations()
        list_of_three.clear()
        update_list_of_three()


    return render(request, 'creating_organization.html', {'organization_form': organization_form,
                                                         'error': error})

# updating json file function after deleting organization
def update_json(name):
    # deleting oragnization
    with open('package.json', 'r') as read_file:
        # load data from json file to data variable
        data = json.load(read_file)

        # assigning data from data to organizations variable
        organizations = data['organizations']

        # initializing index of element we want to delete
        index = -1

        # finding orgaization to delete
        for i in range(len(organizations)):
            if name == organizations[i]['name']:
                index = i

        # pop out organization from the list
        organizations.pop(index)

        # rewriting json file
        # forming dictionary to load in json
        org = dict(organizations=organizations)

    # oppening json file and adding information to it
    with open('package.json', 'w') as write_file:
        json.dump(org, write_file)

# view functuin for editing organziation
def edit_organization(request):
    # getting organization model by name
    org_id = request.GET.get('id')
    #organization = Organization.objects.get(pk=org_id)
    organization = get_object_or_404(Organization, pk=org_id)

    # old organization name
    old_name = organization.name

    if request.method == 'POST':
        organization_form = Editing_Organization(request.POST, instance=organization)

        # assigning new organization info
        organization_new_name = request.POST.get('name')
        organization_new_year_of_est = request.POST.get('year_of_est')
        organization_new_location = request.POST.get('location')
        organization_new_brief_decriptiton = request.POST.get('brief_description')

        # editing organization
        organization.name = organization_new_name
        organization.location = organization_new_location
        organization.year_of_est = organization_new_year_of_est
        organization.brief_description = organization_new_brief_decriptiton
        organization.save()

        # updating json
        update_json(old_name)

    else:
        organization_form = Editing_Organization(instance=organization)


    return render(request, 'editing_organizations.html', {'organization_form': organization_form})

# veiw function for deleting organization
def delete_organization(request):
    # getting name of object we want to delete
    name = request.GET.get('name')

    # finding object we want to delete
    obj_to_delete = Organization.objects.get(name=name)

    # delete object from sql database
    obj_to_delete.delete()

    # updating list of three
    list_of_three.clear()
    update_list_of_three()

    # updating json database and getting new organization dict
    new_orgs = update_json(name)

    return render(request, 'index.html', {'organizations': list_of_three})

# edit person
def create_person(request):
    # creating user formcl
    person_form = Editing_Person()

    return render(request, 'creating_user.html', {'person_form': person_form})

def creating_day(request):
    # creating users day
    days_form = Editing_Days()

    return render(request, 'creating_days.html', {'days_form': days_form})

# view function for home page
def home(request):
    # creating dict to give it
    # as third parameter to
    # render function
    vars = dict(organizations=list_of_three)

    return render(request, 'index.html', vars)