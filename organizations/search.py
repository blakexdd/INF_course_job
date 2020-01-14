import wikipedia
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
import re
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from stop_words import get_stop_words
from nltk.corpus import stopwords
import pickle


org_names = ['yandex', 'apple', 'samsung', 'mercedes',
             'Oracle', 'Walt Disney', 'General Electric']

y_dict = {}

for (i, org) in enumerate(org_names):
    y_dict[org] = i

print(y_dict)

pages_list = []

stop_words = list(get_stop_words('ru'))
nltk_words = list(stopwords.words('russian'))
stop_words.extend(nltk_words)

# initializing features and samples lists
X = []
y = []

def collect_data(org_names):
    # setting language of wiki pages to Russian
    wikipedia.set_lang('Ru')


    # getting pages describing our organizations
    for org in org_names:
        org_pages = wikipedia.search(org, results=17)
        for page in org_pages:
            pages_list.append((page, org))

    # collection features and samples
    for org_page, org_name in pages_list:
        # print('Org_page: ', org_page)
        # print('Summary: ', (wikipedia.page(org_name)).summary)
        # print('=======')
        X.append((wikipedia.page(org_page)).summary)
        y.append(y_dict[str(org_name)])

    return X, y

def text_processing(X):
    new_X = []

    for i in X:
        doc = re.sub(r'\d', ' ', str(i))

        doc = re.sub(r'\s+[a-zA-Z]\s+', ' ', doc)

        doc = re.sub(r'\^[a-zA-Z]\s+', ' ', doc)

        doc = re.sub(r'\s+', ' ', doc, flags=re.I)

        doc = re.sub('\n', ' ', doc)

        doc = doc.lower()

        new_X.append(doc)

    return new_X

data = collect_data(org_names)
preprocessed_data = text_processing(data[0])

X_train, X_test, y_train, y_test = train_test_split(preprocessed_data, data[1])
vectorizer = CountVectorizer()
X_train_transformed = vectorizer.fit_transform(X_train)
X_test_transformed = vectorizer.transform(X_test)

pipe = Pipeline([('vect', CountVectorizer(min_df = 3, stop_words=stop_words)),
                ('tfidf', TfidfTransformer()),
                ('clf', SVC(random_state=1))])

parameters = {'vect__ngram_range': [(1, 1), (1, 2)],
             'tfidf__use_idf': (True, False),
             'clf__C': [0.001, 0.01, 0.1, 1, 10, 100, 1000]}

grid_s = GridSearchCV(pipe, parameters, n_jobs=-1, verbose=1)

grid_s_fit = grid_s.fit(X_train, y_train)

y_dict_trans = {}

for (org, i) in enumerate(org_names):
    y_dict_trans[org] = i

predicted = grid_s_fit.predict(X_test)

accuracy_score(y_test, predicted)

pickle.dump(grid_s_fit, open('model.sav', 'wb'))