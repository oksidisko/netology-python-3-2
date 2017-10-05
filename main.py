import json
import re
import os
import chardet


def get_words(text):
    return re.compile('\w+').findall(text)


def get_long_strings(strings, min_length):
    result = [];
    for item in strings:
        if len(item) >= min_length:
            result.append(item)
    return result


def get_news_files_list(path):
    files = [];
    directory = os.fsencode(path)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            files.append(path + '/' + filename);
    return files;


def read_json_from_file(path):
    with open(os.fsencode(filePath), 'rb') as f:
        data = f.read();
        chardet_result = chardet.detect(data)

        return json.loads(data.decode(chardet_result['encoding']))
    return data


def index_words(words):
    result = {}
    for word in words:
        word = word.lower();
        if word not in result:
            result[word] = 0
        result[word] += 1
    result = [(i, result[i]) for i in result]
    return sorted(result, key=lambda x: x[1], reverse=True)[:10]


for filePath in get_news_files_list('data'):
    data = read_json_from_file(filePath)
    channel_description = data['rss']['channel']['description']
    print('=== ' + channel_description)
    long_words = []
    for item in data['rss']['channel']['items']:
        long_words += get_long_strings(get_words(item['description'] + ' ' + item['title']), 6)

    index = index_words(long_words)
    for row in index:
        print('{word}: {count}'.format(word=row[0], count=row[1]))
    print('\n')
