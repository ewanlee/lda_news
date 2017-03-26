import io
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import  LatentDirichletAllocation

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print 'Topic #%d:' % topic_idx
        print ' '.join([feature_names[i]
                        for i in topic.argsort()[: -n_top_words - 1 : -1]])
        print

with io.open('splitted_news.pkl', 'rb') as f:
    splitted_news = pickle.load(f)

id_title = {}
data_samples = []
id = 0

for key, value in splitted_news.items():
    id_title[id] = key
    data_samples.append(value)
    id += 1

with io.open('title_id.pkl', 'wb') as f:
    pickle.dump(id_title, f)

# print data_sample[342]
# print id_title[342]

# Use tf (raw term count) features for LDA
print("Extracting tf feature for LDA...")
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=1000)

tf = tf_vectorizer.fit_transform(data_samples)
# print tf_vectorizer.get_feature_names()[456]

print 'Fitting LDA models with tf features...'
lda = LatentDirichletAllocation(n_topics=10, max_iter=20,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)
lda.fit(tf)

print '\nTopic in LDA model:'
tf_feature_names = tf_vectorizer.get_feature_names()
print_top_words(lda, tf_feature_names, 100)

# Transfrom to topic probabilities
topic_prob = np.array(lda.transform(tf))
news_topics = []
for probs in topic_prob:
    news_topics.append(np.where(probs >= 0.5)[0].tolist())

with io.open('news_topics.pkl', 'wb') as f:
    pickle.dump(news_topics, f)
