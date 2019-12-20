
from gensim.models import FastText
from .models import Organization

# initializing list of organization names
organizations_names_list = []

def get_data():
    # getting all organizations
    organizations = Organization.objects.all()

    # filling organization list names
    for org in organizations:
        organizations_names_list.append(org.name)

# initializing fasttext model
model = FastText(size=4, min_count=1, window=3)

# building vocablulary
model.build_vocab(organizations_names_list)

# training model
model.train(sentences=organizations_names_list, total_examples=len(organizations_names_list), epochs=10)

print("Most similar to yandex", model.most_similar('Яйндекс'))