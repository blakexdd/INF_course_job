from django.shortcuts import render
import json

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