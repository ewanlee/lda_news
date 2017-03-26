import os
from bosonnlp import BosonNLP
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import  LatentDirichletAllocation


news_dir = '/home/ewan/PycharmProjects/news_spider/news/'
file_list = os.listdir(news_dir)

nlp = BosonNLP('FuHSE7Vf.13924.jadflTdrQLWx')
splitted_titles = []

SIZE = len(file_list)
count = 0

stop_tags = ['w', 't', 'q', 'u', 'k', 'h', 'o', 'y', 'c', 'p', 'd', 'r']

for title in file_list:
    count += 1
    if count % (SIZE / 100) == 0:
        print count
    result = nlp.tag(title)
    words = ''
    for index, word in enumerate(result[0]['word']):
        stop = False
        for tag in stop_tags:
            if tag in result[0]['tag'][index]:
                stop = True
                break
        if stop is False:
            words += word + ' '

    splitted_titles.append(words)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print 'Topic #%d:' % topic_idx
        print ' '.join([feature_names[i]
                        for i in topic.argsort()[: -n_top_words - 1 : -1]])
        print


# Use tf (raw term count) features for LDA
print("Extracting tf feature for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=1000)

tf = tf_vectorizer.fit_transform(splitted_titles)
# print tf_vectorizer.get_feature_names()[456]

print 'Fitting LDA models with tf features...'
lda = LatentDirichletAllocation(n_topics=5, max_iter=20,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(tf)

print '\nTopic in LDA model:'
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 20)

# Transfrom to topic probabilities
topic_prob = np.array(lda.transform(tf))
news_topics = []
for probs in topic_prob:
    news_topics.append(np.where(probs >= 0.1)[0].tolist())

topics = {}
for topic in xrange(5):
    topics[topic] = []

for index, new_topics in enumerate(news_topics):
    for topic in new_topics:
        topics[topic].append(index)

for new_id in topics[0][:30]:
    print splitted_titles[new_id]

for key in topics:
    print key


