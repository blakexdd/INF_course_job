from django.shortcuts import get_object_or_404, render
from .models import Organization
from .models import Dates, Person
from django.contrib.auth.models import User
import json

new_id = 0

# creating organizations from json file
with open("package.json") as packege:
    # assigning data from json file
    # to data variable
    data = json.load(packege)

    # loading Organiations
    existing_organizations = Organization.objects.all()

    # creating list of existing organizations
    existing_orgs_names = []
    for existing_org in existing_organizations:
        existing_orgs_names.append(existing_org.name)

    print(existing_orgs_names)


    # going through all organizations in
    # json data base and checking if we updated
    # and loaded all organizations
    # if we don't find name of organizations that placed in json file
    # at our site, we add this record and if we find a name
    # we simply update previous object, so each time when we start our
    # server, organizations data base updates
    for new_organization in data['organizations']:
        if new_organization['name'] not in existing_orgs_names:
            # print(new_organization['name'], 'is not in existing organizations')
            # creating description string
            str_desc = "".join(new_organization['brief_decription'])

            # if organization doesn't exist, add new organization
            new_org = Organization(name=new_organization['name'], year_of_est=new_organization['year_of_establishing'],
                                   location='{} {} {}'.format(new_organization['location']['index'],
                                                              new_organization['location']['city'],
                                                              new_organization['location']['adress']),
                                   brief_description=str_desc)
            new_org.save()

            # creating particular person in the company from the database
            for person in new_organization['personel']:
                # creating new person
                new_person = Person(name=person['name'], surname=person['surname'], middlename=person['middlename'],
                                    date_of_birth=person['date_of_birth'], post=person['post'], hours_per_week=person['hours_per_week'])

                # saving new person
                new_person.save()

                # deleting old user
                old_user = \
                    User.objects.filter(username=''.join([person['name'], person['surname'], person['middlename']]))[0]
                old_user.delete()
                # creating user with save id as person has
                new_user = User.objects.create_user(
                    username=''.join([person['name'], person['surname'], person['middlename']]),
                    id=new_person.id)
                print('New user: ', new_user)
                print("New users name: ", new_user.id)

                print('New person: ', new_person)

                # saving new user
                new_user.save()

                # creating particular date in persons schedule
                for day in person['days']:
                    # creatin new day of the week
                    new_day = Dates(day=day['name'], start=day['start'], end=day['end'])

                    new_day.save()

                    # adding new day to persons schedule
                    new_person.days.add(new_day)

                 # adding new person to organization
                new_org.person.add(new_person)

        else:
            # print(new_organization['name'], 'is in EXISTING organizations')
            # print('new year_of_est: ', new_organization['year_of_establishing'])

            # creating description string
            str_desc = "".join(new_organization['brief_decription'])
            #print('Desc str', str_desc)

            # if organizations exists, modify it's fields
            Organization.objects.filter(name=new_organization['name']).update(year_of_est=new_organization['year_of_establishing'],
                                                                              location='{} {} {}'.format(new_organization['location']['index'],
                                                             new_organization['location']['city'],
                                                              new_organization['location']['adress']),
                                                                              brief_description=str_desc)

            # deleting old instances
            old_personel = Organization.objects.filter(name=new_organization['name'])[0].person.all()
            old_personel.delete()


            # creating particular person in the company from the database
            for person in new_organization['personel']:
                new_person = Person(name=person['name'], surname=person['surname'], middlename=person['middlename'],
                                    date_of_birth=person['date_of_birth'], post=person['post'],
                                    hours_per_week=person['hours_per_week'])

                # saving new person
                new_person.save()

                # deleting old user
                old_user = \
                User.objects.filter(username=''.join([person['name'], person['surname'], person['middlename']]))[0]
                old_user.delete()
                # creating user with save id as person has
                new_user = User.objects.create_user(username=''.join([person['name'], person['surname'], person['middlename']]),
                                                    id=new_person.id, password=1234)
                print('New user: ', new_user)
                print("New users name: ", new_user.id)

                print('New person: ', new_person)

                # saving new user
                new_user.save()


                # deleting old instances
                old_days = new_person.days.all()
                old_days.delete()

                # creating particular date in persons schedule
                for day in person['days']:
                    new_day = Dates(day=day['name'], start=day['start'], end=day['end'])
                    # saving new day
                    new_day.save()
                    print('New persons ', new_person, 'day ', new_day)

                    new_person.days.add(new_day)

                # adding particular person to organization
                Organization.objects.filter(name=new_organization['name'])[0].person.add(new_person)




            # adding day to persons schedule
            #new_person.days.add(new_day)

            #Organization.objects.filter(name=new_organization['name'])[0].save()

            # print('Organization: ', Organization.objects.filter(name=new_organization['name'])[0].name)
            # print('Persons name: ', Organization.objects.filter(name=new_organization['name'])[0].person.all()[0].name)
            # print(Organization.objects.filter(name=new_organization['name']))



    #d1 = Dates(day='Monday', start='9:00', end='18:00')
    #d2 = Dates(day='Thursday', start='9:00', end='18:00')
    #d1.save()
    #d2.save()
    #person1 = Person(name='Vlaimir', surname='Gololobov', middlename='Vladimirovich', date_of_birth='06.08.2001',
    #               post='student',hours_per_week=45)
    #person1.save()
    #person1.days.add(d1, d2)

    #print('person1: ', person1.name, ' ', person1.surname, ' ', person1.days.all()[0].day, person1.days.all()[1].day )


# view function for organizations
def orgs(request):
    orgs = Organization.objects.all()
    return render(request, 'organizations/organizations.html',
                              {'organizations': orgs})

# view function for personal cabinet
def pers_cabinet(request, user_id):
    # assigning current user to user variable
    user = request.user

    # getting user from database
    for organization in Organization.objects.all():
        for person in organization.person.all():
            if user.id == person.id:
                new_user = person


    return render(request, 'personal_cab.html', {'person': new_user})


# view function for particular organization
def one_org(request, org_id):
    # assigning Organization object to org variable
    org = get_object_or_404(Organization, pk=org_id)

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
        name = org.name,
        year_of_est = org.year_of_est,
        location = org.location,
        brief_description= org.brief_description,
        personel = org.person.all(),
        pers = personal
    )

    return render(request, 'organizations/one_org.html', vars)
