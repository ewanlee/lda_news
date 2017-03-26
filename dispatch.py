import pickle
import io

with io.open('news_topics.pkl', 'rb') as f:
    news_topics = pickle.load(f)

with io.open('title_id.pkl', 'rb') as f:
    title_id = pickle.load(f)

topics = {}
for topic in xrange(10):
    topics[topic] = []

for index, new_topics in enumerate(news_topics):
    for topic in new_topics:
        topics[topic].append(index)

for new_id in topics[9][:30]:
    print title_id[new_id]

