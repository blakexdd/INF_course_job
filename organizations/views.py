from django.shortcuts import get_object_or_404, render
from .models import Organization
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
        else:
            # print(new_organization['name'], 'is in EXISTING organizations')
            # print('new year_of_est: ', new_organization['year_of_establishing'])
            # if organizations exists, modify it's fields
            Organization.objects.filter(name=new_organization['name']).update(year_of_est=new_organization['year_of_establishing'],
                                                                              location='{} {} {}'.format(new_organization['location']['index'],
                                                             new_organization['location']['city'],
                                                              new_organization['location']['adress']))
            #print(Organization.objects.filter(name=new_organization['name']))



# view function for organizations
def orgs(request):
    orgs = Organization.objects.all()
    return render(request, 'organizations/organizations.html',
                              {'organizations': orgs})

# view function for particular organization
def one_org(request, org_id):
    # assigning Organization object to org variable
    org = get_object_or_404(Organization, pk=org_id)

    # creating dict with organization fields
    vars = dict(
        name = org.name,
        year_of_est = org.year_of_est,
        location = org.location
    )

    return render(request, 'organizations/one_org.html', vars)
