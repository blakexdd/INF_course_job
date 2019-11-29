from django.shortcuts import get_object_or_404, render
from django.template import RequestContext
from .models import Organization


# Create your views here.

def orgs(request):
    orgs = Organization.objects.all()
    return render(request, 'organizations/organizations.html',
                              {'organizations': orgs})

def one_org(request, org_id):
    org = get_object_or_404(Organization, pk=org_id)

    vars = dict(
        name = org.name,
        year_of_est = org.year_of_est
    )

    return render(request, 'organizations/one_org.html', vars)
