from bosonnlp import BosonNLP
import pickle
import re
import sys

with open('news.pkl', 'rb') as f:
    news = pickle.load(f)

nlp = BosonNLP('FuHSE7Vf.13924.jadflTdrQLWx')
splitted_news = {}

SIZE = len(news)
count = 0

green_tags = ['n', 's', 'v']

for key, value in news.items():
    count += 1
    if count % (SIZE / 100) == 0:
        print count
    result = nlp.tag([value])
    words = ''
    for index, word in enumerate(result[0]['word']):
        green = False
        for tag in green_tags:
            if tag in result[0]['tag'][index]:
                green = True
                break
        if green:
            words += word + ' '

    # print words
    # splitted_news[key] = re.split(ur'\s+', words)
    # print sys.getdefaultencoding()
    splitted_news[key] = words

with open('splitted_news.pkl', 'wb') as f:
    pickle.dump(splitted_news, f, 0)

