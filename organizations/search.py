<<<<<<< HEAD
import wikipedia
from sklearn.feature_extraction import CountVectorizer

org_names = ['yandex', 'apple', 'samsung', 'mercedes', 'vk', 'ibm', 'at&t', 'McDonald’s', 'Coca-Cola',
             'Oracle', 'Walt Disney', 'General Electric']
pages_list = []


def collect_data(org_names):
    # setting language of wiki pages to Russian
    wikipedia.set_lang('Ru')

    # initializing features and samples lists
    X = []
    y = []

    # getting pages describing our organizations
    for org in org_names:
        org_pages = wikipedia.search(org, results=2)
        for page in org_pages:
            pages_list.append((page, org))

    # collection features and samples
    for org_page, org_name in pages_list:
        # print('Org_name: ', org_name)
        # print('Org_page: ', org_page)
        # print('Summary: ', (wikipedia.page(org_name)).summary)
        # print('=======')
        X.append((wikipedia.page(org_page)).summary)
        y.append(org_name)

    return X, y

def build_vectors():
    X, y = collect_data(org_names)

    vectorizer = CountVectorizer()

collect_data(org_names)





=======
>>>>>>> 2fee59dbbb7187bcd710c0b2e9fb1deacd261e68
