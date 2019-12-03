from django.shortcuts import get_object_or_404, render
from .models import Organization
from .models import Dates, Person
import json

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
            # if organization doesn't exist, add new organization
            new_org = Organization(name=new_organization['name'], year_of_est=new_organization['year_of_establishing'],
                                   location='{} {} {}'.format(new_organization['location']['index'],
                                                              new_organization['location']['city'],
                                                              new_organization['location']['adress']))
            new_org.save()

            # creating particular person in the company from the database
            for person in new_organization['personel']:
                # creating new person
                new_person = Person(name=person['name'], surname=person['surname'], middlename=person['middlename'],
                                    date_of_birth=person['date_of_birth'], post=person['post'], hours_per_week=person['hours_per_week'])

                new_person.save()

                # adding new person to organization
                new_org.person.add(new_person)

                # creating particular date in persons schedule
                for day in person['days']:
                    # creatin new day of the week
                    new_day = Dates(day=day['name'], start=day['name'], end=day['end'])

                    new_day.save()

                    # adding new day to persons schedule
                    new_person.days.add(new_day)

        else:
            # print(new_organization['name'], 'is in EXISTING organizations')
            # print('new year_of_est: ', new_organization['year_of_establishing'])
            # if organizations exists, modify it's fields
            Organization.objects.filter(name=new_organization['name']).update(year_of_est=new_organization['year_of_establishing'],
                                                                              location='{} {} {}'.format(new_organization['location']['index'],
                                                             new_organization['location']['city'],
                                                              new_organization['location']['adress']))

            # deleting old instances
            old_personel = Organization.objects.filter(name=new_organization['name'])[0].person.all()
            old_personel.delete()

            # creating particular person in the company from the database
            for person in new_organization['personel']:
                new_person = Person(name=person['name'], surname=person['surname'], middlename=person['middlename'],
                                    date_of_birth=person['date_of_birth'], post=person['post'],
                                    hours_per_week=person['hours_per_week'])

                new_person.save()

                print('New person: ', new_person)
                # adding particular person to organization
                Organization.objects.filter(name=new_organization['name'])[0].person.add(new_person)

                # deleting old instances
                old_days = new_person.days.all()
                old_days.delete()

                # creating particular date in persons schedule
                for day in person['days']:
                    new_day = Dates(day=day['name'], start=day['name'], end=day['end'])
                    # saving new day
                    new_day.save()
                    print('New persons ', new_person, 'day ', new_day)

                    new_person.days.add(new_day)


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

# view function for particular organization
def one_org(request, org_id):
    # assigning Organization object to org variable
    org = get_object_or_404(Organization, pk=org_id)

    # parsing schedule for personel
    #personal_dates = []
    #for i in range(len(org.person.all())):
    #    personal_dates.append(org.person.all()[i].days.all())

    #print('Parsed list of dates for user: ', personal_dates)

    print("Getting schedule of the company: ", org.person.all()[0].days.all())
    print("Printing date: ", org.person.all()[0].days.all()[0].day)
    #print('Getting peesons of the company: ', org.person.all())

    # creating dict with organization fields
    vars = dict(
        name = org.name,
        year_of_est = org.year_of_est,
        location = org.location,
        personel = org.person.all(),
    )

    return render(request, 'organizations/one_org.html', vars)
