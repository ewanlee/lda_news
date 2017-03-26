import os
import io
import pickle

# Get news file path
news_dir = '/home/ewan/PycharmProjects/news_spider/news/'
file_list = os.listdir(news_dir)


# Get the news dict
news = {}
for file in file_list:
    with io.open(news_dir + file, 'r') as f:
        news[file] = f.read()

with open('news.pkl', 'wb') as f:
    pickle.dump(news, f)


