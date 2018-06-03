# -*- coding: utf-8 -*-
import csv
import random
import time
import os
import re

stopwords = set()


def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for stopword in lines:
            stopwords.add(stopword)


def separate_sentences(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)


def get_file_list(dir):
    file_list = []
    filenames = os.listdir(dir)
    for filename in filenames:
        if not filename.startswith('.'):
            file_list.append(os.path.join(dir, filename))
    print('get file list: {}'.format(file_list))
    return file_list


def write(filename, documents):
    with open(filename, 'a', encoding='utf-8', newline='') as file:
        for document in documents:
            file.write(document + '\n')

def clean_text(text):
    cleaned_text = re.sub('[a-zA-Z]', '', text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]',
                          '', cleaned_text)
    return cleaned_text

def remove_reporter(contents):
    contents = re.sub('사진뉴스1', '', contents).strip()
    contents = re.sub('인천=연합뉴스', '', contents).strip()
    contents = re.sub('사진=연합뉴스', '', contents).strip()
    contents = re.sub('연합뉴스 제공', '', contents).strip()
    contents = re.sub('연합뉴스', '', contents).strip()
    contents = re.sub('이제원 기자', '', contents).strip()
    contents = re.sub('전형주 인턴기자', '', contents).strip()
    contents = re.sub('ⓒ 남소연', '', contents).strip()
    contents = re.sub('전형주 인턴기자', '', contents).strip()




def make_train_data(filename):
    file = open(filename, 'r', encoding='utf-8')
    lines = csv.reader(file, delimiter='\t')

    results = []

    print('before make_train_data')
    start_time = time.time()
    for idx, line in enumerate(lines):
        if (idx % 1000) == 0:
            print('step: {}, time: {:f}'.format(idx, (time.time() - start_time)))
            start_time = time.time()

        if len(line) == 5 and line[1]:
            category = line[1].strip()
            if category == 'IT':
                continue

            temp_summary_list = separate_sentences('. ', '? ', '! ', '\n', '.\n')(''.join(line[4].splitlines()))
            summaries = ''.join([summary.strip() for summary in temp_summary_list[:1]])

            if len(summaries) > 50 or len(summaries) < 20:
                continue;

            contents = separate_sentences('. ', '? ', '! ', '\n', '.\n', '\t')(''.join(line[3].splitlines()))

            if len(contents) > 4:
                contents = contents[1:4]
                if len(contents[0]) < 8:
                    continue

            contents = ' '.join(content.strip() for content in contents)

            if len(contents) < 50:
                continue;

            p = re.compile('\【.*?\=')
            contents = re.sub(p, '', contents).strip()
            p = re.compile('\<.*?\>')
            contents = re.sub(p, '', contents).strip()
            summaries = re.sub(p, '', summaries).strip()
            p = re.compile('\[.*?\]')
            contents = re.sub(p, "", contents).strip()
            summaries = re.sub(p, "", summaries).strip()
            p = re.compile('\【.*?\】')
            contents = re.sub(p, "", contents).strip()
            summaries = re.sub(p, "", summaries).strip()
            p = re.compile('\(.*?\)')
            contents = re.sub(p, "", contents).strip()
            summaries = re.sub(p, "", summaries).strip()
            p = re.compile('.*?\ 기자 =')
            contents = re.sub(p, "", contents).strip()
            contents = re.sub(p, "", contents).strip()
            # summaries = re.sub('[-=.#/?:$}]', '', summaries).strip()
            p = re.compile('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
            contents = re.sub(p, "", contents).strip()
            contents = re.sub('[-=.#/?:$}◆⑤]', '', contents).strip()

            contents = remove_reporter(contents)

            contents = separate_sentences('. ', '? ', '! ', '\n', '.\n')(''.join(contents))
            contents = ' '.join(content.strip() for content in contents)

            contents = clean_text(contents)
            summaries = clean_text(summaries)

            if summaries.__contains__('[') or summaries.__contains__('(') or summaries.__contains__(
                    '<') or summaries.__contains__(
                '→') or summaries.__contains__('↓') or summaries.__contains__('↑'):
                continue
            if contents.__contains__('[') or contents.__contains__('(') or contents.__contains__(
                    '<') or contents.__contains__('#') or contents.__contains__('◀') or contents.__contains__(
                '【') or contents.__contains__('@'):
                continue

            results.append([summaries.strip(), contents.strip(), (category + ', ' + contents.strip())])

    return results


def write_train_data(train_data_list):
    titles = []
    article = []
    cat_article = []
    for row_data in train_data_list:
        titles.append(row_data[0])
        article.append(row_data[1])
        cat_article.append(row_data[2])

    total_documents = len(train_data_list) - 2000
    train_index = int(total_documents * 0.9)
    valid_index = int(total_documents * 0.1) + train_index

    if not os.path.exists(output_dir + '/train'):
        os.makedirs(output_dir + '/train')

    if not os.path.exists(output_dir + '/cat'):
        os.makedirs(output_dir + '/cat')

    write(output_dir + '/train/train.title.txt', titles[:train_index])
    write(output_dir + '/train/train.article.txt', article[:train_index])
    write(output_dir + '/train/valid.title.filter.txt', titles[train_index:valid_index])
    write(output_dir + '/train/valid.article.filter.txt', article[train_index:valid_index])
    write(output_dir + '/train/test.title.txt', titles[valid_index:])
    write(output_dir + '/train/test.giga.txt', article[valid_index:])

    write(output_dir + '/cat/train.title.txt', titles[:train_index])
    write(output_dir + '/cat/train.article.txt', cat_article[:train_index])
    write(output_dir + '/cat/valid.title.filter.txt', titles[train_index:valid_index])
    write(output_dir + '/cat/valid.article.filter.txt', cat_article[train_index:valid_index])
    write(output_dir + '/cat/test.title.txt', titles[valid_index:])
    write(output_dir + '/cat/test.giga.txt', cat_article[valid_index:])


if __name__ == '__main__':
    intput_dir = '/Users/unbreaks/git/seq2seq_summarization/crawler/data'
    output_dir = '/Users/unbreaks/Desktop'
    file_list = get_file_list(intput_dir)

    train_data_list = []
    for file in file_list:
        print('process file:{}'.format(file))
        train_data_list += make_train_data(file)
        print('end process file:{}'.format(file))
    print('total train_data_list size is {}'.format(len(train_data_list)))
    random.shuffle(train_data_list)
    write_train_data(train_data_list)
