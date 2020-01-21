from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
import json
from organizations.views import Organization, Person, Dates
from .forms import Loginform
from organizations.forms import Editing_Organization, Editing_Person, Editing_Days, Com_Search
from organizations.views import updating_organizations
import wikipedia
import requests
import re
import pickle

org_names = ['yandex', 'apple', 'samsung', 'mercedes',
             'Oracle', 'Walt Disney', 'General Electric']
y_dict_trans = {}

for (org, i) in enumerate(org_names):
    y_dict_trans[org] = i

t_model = pickle.load(open('model.sav', 'rb'))


def get_data():
    organizations = Organization.objects.all()
    info_list = []

    for org in organizations:
        info_list.append(wikipedia.page(org.name).content)

    print(len(info_list))

    return info_list



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

    # # openning json file to read info from it
    # with open('package.json', 'r') as read_file:
    #     # load data from json file to data variable
    #     data = json.load(read_file)
    #
    #     # assigning data from data to organizations variable
    #     organizations = data['organizations']
    #
    #     # forming dictionary of parameters to give
    #     # it as a third argument to render function
    #     # for index page
    #     dict_index = {'organizations': organizations}

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

        if organization_form.cleaned_data.get('year_of_est') == 'Auto' or \
            organization_form.cleaned_data.get('location') == 'Auto' or \
                organization_form.cleaned_data.get('brief_description') == 'Auto':
            wikipedia.set_lang('Ru')
            search_page = wikipedia.search(organization_name)[0]
            page = wikipedia.page(search_page)
            page_url = page.url
            url = requests.get(page_url).text

            soup = BeautifulSoup(url, 'html.parser')

            info_table = soup.find('table', {'class': 'infobox vcard'})

            table_row = info_table.find_all('tr')

        if organization_form.cleaned_data.get('year_of_est') != 'Auto':
            organization_year_of_est = organization_form.cleaned_data.get('year_of_est')
        else:
            for row in table_row:
                title = row.find('th', {'class': 'plainlist'})
                if title != None:
                    if title.text == 'Основание':
                        year_of_est = row.find('td', {'class': 'plainlist'})
                        organization_year_of_est = year_of_est.text

        if organization_form.cleaned_data.get('location') != 'Auto':
            organization_location = organization_form.cleaned_data.get('location')
        else:
            for row in table_row:
                title = row.find('th', {'class': 'plainlist'})
                if title != None:
                    if title.text == 'Расположение':
                        location = row.find('td', {'class': 'plainlist'})
                        organization_location = location.text

        if organization_form.cleaned_data.get('brief_description') != 'Auto':
            organization_brief_description = organization_form.cleaned_data.get('brief_description')
        else:
            organization_brief_description = (page.summary)[:499]

        # forming organization dictionary
        # new_organization = dict(name=organization_name,
        #                         year_of_establishing=organization_year_of_est,
        #                         location=dict(index=organziation_index,
        #                                       city=organization_city,
        #                                       adress=organization_adress),
        #                         brief_decription=organization_brief_description)

        if Organization.objects.filter(name=organization_name):
            error = 'Огранизация уже существует'
        else:
            new_org = Organization(name=organization_name,
                                   year_of_est=organization_year_of_est,
                                   location=organization_location,
                                   brief_description=organization_brief_description)
            new_org.save()
            print(new_org)

    list_of_three.clear()
    update_list_of_three()

        # # opening json file to add there information about new organization
        # with open('package.json', 'r') as read_file:
        #     # load data from json file to data variable
        #     data = json.load(read_file)
        #
        #     # assigning data from data to organizations variable
        #     organizations = data['organizations']
        #
        #     # initializing flag if organization exists
        #     flag = 0
        #
        #     # going through organizations and finding created organization in list
        #     for i in range(len(organizations)):
        #         if organizations[i]['name'] == organization_name:
        #             flag = i
        #
        #     if flag == 0:
        #         organizations.append(new_organization)
        #     else:
        #         error = 'Organization already exists'
        #
        # #forming dictionary to load in json
        # org = dict(organizations=organizations)
        #
        # # oppening json file and adding information to it
        # with open('package.json', 'w') as write_file:
        #     json.dump(org, write_file)
        #     #print('Organization[-1]:', organizations[-1])
        #
        #     #print('==================================')
        #     #print(organizations)
        #
        # #print(new_organization)
        #
        # updating_organizations()
        # list_of_three.clear()
        # update_list_of_three()


    return render(request, 'create_organization.html', {'organization_form': organization_form,
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
        # update_json(old_name)

    else:
        organization_form = Editing_Organization(instance=organization)


    return render(request, 'editing_organizations.html', {'organization_form': organization_form})

# veiw function for editing person info
def edit_person(request):
    # getting organization model by name
    person_id = request.GET.get('id')
    person = get_object_or_404(Person, pk=person_id)

    if request.method == 'POST':
        person_form = Editing_Person(request.POST, instance=person)

        # assigning new organization info
        person_new_name = request.POST.get('name')
        person_new_surname = request.POST.get('surname')
        person_new_middlename = request.POST.get('middlename')
        person_new_date_of_birth = request.POST.get('date_of_birth')
        person_new_post = request.POST.get('post')
        person_new_hours_per_week = request.POST.get('hours_per_week')

        # editing organization
        person.name = person_new_name
        person.surname = person_new_surname
        person.middlename = person_new_middlename
        person.date_of_birth = person_new_date_of_birth
        person.post = person_new_post
        person.hours_per_week = person_new_hours_per_week
        person.save()

        # updating json
        # update_json(old_name)

    else:
        person_form = Editing_Person(instance=person)

    return render(request, 'editing_person.html', {'person_form': person_form})

# view function for editing day
def edit_days(request):
    # getting organization model by name
    day_id = request.GET.get('id')
    day = get_object_or_404(Dates, pk=day_id)

    if request.method == 'POST':
        day_form = Editing_Days(request.POST, instance=day)

        # assigning new organization info
        day_new_name = request.POST.get('day')
        day_new_start = request.POST.get('start')
        day_new_end = request.POST.get('end')

        # editing organization
        day.day = day_new_name
        day.start = day_new_start
        day.end = day_new_end
        day.save()

    else:
        day_form = Editing_Days(instance=day)

    return render(request, 'editing_day.html', {'day_form': day_form})

# view function for deleting person
def delete_person(request):
    # getting persons id and organization name
    person_id = request.GET.get('id')
    org_name = request.GET.get('name')

    # finding person in database
    person_to_delete = Person.objects.get(pk=person_id)

    # deleting person
    person_to_delete.delete()

    org = get_object_or_404(Organization, name=org_name)

    # parsing schedule for personel
    personal = []
    parsed_dates = []
    for person in org.person.all():
        print('Person: ', person)
        for days in person.days.all():
            print('Days: ', days)
            parsed_dates.append(days)
        personal.append([person, parsed_dates])

    print('List of persons and dates: ', personal)

    # creating dict with organization fields
    vars = dict(
        name=org.name,
        year_of_est=org.year_of_est,
        location=org.location,
        brief_description=org.brief_description,
        personel=org.person.all(),
        pers=personal
    )

    return render(request, 'organizations/one_org.html', vars)

# view function for deleting day
def delete_day(request):
    # getting days id and organizaiton name
    days_id = request.GET.get('id')
    org_name = request.GET.get('name')

    # findgin day in database
    day_to_delete = Dates.objects.get(pk=days_id)

    # deleting day
    day_to_delete.delete()

    org = get_object_or_404(Organization, name=org_name)

    # parsing schedule for personel
    personal = []
    parsed_dates = []
    for person in org.person.all():
        print('Person: ', person)
        for days in person.days.all():
            print('Days: ', days)
            parsed_dates.append(days)
        personal.append([person, parsed_dates])

    print('List of persons and dates: ', personal)

    # creating dict with organization fields
    vars = dict(
        name=org.name,
        year_of_est=org.year_of_est,
        location=org.location,
        brief_description=org.brief_description,
        personel=org.person.all(),
        pers=personal
    )

    return render(request, 'organizations/one_org.html', vars)

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

    # # updating json database and getting new organization dict
    # new_orgs = update_json(name)

    return render(request, 'index.html', {'organizations': list_of_three})

# edit person
def create_person(request):

    # getting organization name
    org_name = request.GET.get('name')

    # getting organization
    organization = Organization.objects.filter(name=org_name)[0]

    # creating user formcl
    person_form = Editing_Person(request.POST or None)

    # getting data from form and creating person instance
    if person_form.is_valid():
        person_name = person_form.cleaned_data.get('name')
        person_surname = person_form.cleaned_data.get('surname')
        person_middlename = person_form.cleaned_data.get('middlename')
        person_date_of_birth = person_form.cleaned_data.get('date_of_birth')
        person_post = person_form.cleaned_data.get('post')
        person_hours_per_week = person_form.cleaned_data.get('hours_per_week')

        print(person_name, person_surname, person_date_of_birth, person_post)

        # creating person instance
        new_person = Person(name=person_name,
                            surname=person_surname,
                            middlename=person_middlename,
                            date_of_birth=person_date_of_birth,
                            post=person_post,
                            hours_per_week=person_hours_per_week)

        # saving new person
        new_person.save()

        # adding new person to organization
        organization.person.add(new_person)

    return render(request, 'create_person.html', {'person_form': person_form})

def creating_day(request):
    # getting person name
    person_id = request.GET.get('id')
    print('Id: ', person_id)
    print('All perons: ', Person.objects.filter(pk=person_id))

    # getting person
    person = Person.objects.filter(pk=person_id)[0]

    # creating days form
    days_form = Editing_Days(request.POST or None)

    # getting data from form and creating dat
    if days_form.is_valid():
        day_name = days_form.cleaned_data.get('day')
        day_start = days_form.cleaned_data.get('start')
        day_end = days_form.cleaned_data.get('end')

        # creating new day instance
        new_day = Dates(day=day_name,
                        start=day_start,
                        end=day_end)

        # saving new day instance
        new_day.save()

        # adding day to person
        person.days.add(new_day)

        print('Person days ', person.days.all())

    return render(request, 'create_days.html', {'days_form': days_form})

# view function for home page
def home(request):
    # creating dict to give it
    # as third parameter to
    # render function
    search = Com_Search(request.POST or None)

    # getting all organizations
    organizations = Organization.objects.all()


    print('REQUEST', request.POST.get('query'))
    vars = dict(organizations=list_of_three, search_form=search)

    if request.POST.get('query') != None:
        empty_org = dict(id=-1, name=0)

        # finded_organization = Organization.objects.filter(name=X_lables[model.predict(Search)[0]])[0]
        finded_organization = Organization.objects.filter(name=y_dict_trans[t_model.predict([request.POST.get('query')])[0]])

        vars = dict(organizations=[[finded_organization[0], empty_org, empty_org ]], search_form=search)
    else:
        vars = dict(organizations=list_of_three, search_form=search)

    return render(request, 'index.html', vars)