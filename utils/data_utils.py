# -*- coding: utf-8 -*-
import csv
import random
import time
import os
import re

banned_words = dict()


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

        temp_title_list = line[0].splitlines()
        titles = ''.join([title.strip() for title in temp_title_list])
        category = line[1].strip()
        contents = separate_sentences('. ', '? ', '! ', '\n', '.\n')(''.join(line[2].splitlines()))

        if len(contents) > 2:
            contents = contents[:2]
            if len(contents[0]) < 8:
                continue
        contents = ' '.join(content.strip() for content in contents)

        if contents.endswith('..'):
            continue

        if titles.__contains__('[') or titles.__contains__('(') or titles.__contains__('<') or titles.__contains__(
                '→') or titles.__contains__('↓'):
            continue
        if contents.__contains__('[') or contents.__contains__('(') or contents.__contains__(
                '<') or contents.__contains__('#') or contents.__contains__('◀') or contents.__contains__(
            '【') or contents.__contains__('@'):
            continue

        results.append([titles, contents, (category + ', ' + contents)])

    return results
    print('after make_train_data')


def write_train_data(train_data_list):
    titles = []
    article = []
    cat_article = []
    for row_data in train_data_list:
        titles.append(row_data[0])
        article.append(row_data[1])
        cat_article.append(row_data[2])

    total_documents = len(train_data_list)
    train_index = int(total_documents * 0.8)
    valid_index = int(total_documents * 0.1) + train_index

    # (7:2:1) 비율로 나눔
    # train_set : 0.8
    # valid_set : 0.1
    # test_set : 0.1
    write(output_dir + '/train.title.txt', titles[:train_index])
    write(output_dir + '/train.article.txt', article[:train_index])
    write(output_dir + '/valid.title.filter.txt', titles[train_index:valid_index])
    write(output_dir + '/valid.article.filter.txt', article[train_index:valid_index])
    write(output_dir + '/test.title.txt', titles[valid_index:])
    write(output_dir + '/test.article.txt', article[valid_index:])

    write(output_dir + '/cat_train.title.txt', titles[:train_index])
    write(output_dir + '/cat_train.article.txt', cat_article[:train_index])
    write(output_dir + '/cat_valid.title.filter.txt', titles[train_index:valid_index])
    write(output_dir + '/cat_valid.article.filter.txt', cat_article[train_index:valid_index])
    write(output_dir + '/cat_test.title.txt', titles[valid_index:])
    write(output_dir + '/cat_test.article.txt', cat_article[valid_index:])


if __name__ == '__main__':

    intput_dir = '/Users/unbreaks/Desktop/news'
    output_dir = '/Users/unbreaks/Desktop/trained_data'
    file_list = get_file_list(intput_dir)

    train_data_list = []
    for file in file_list:
        print('process file:{}'.format(file))
        train_data_list += make_train_data(file)
        print('end process file:{}'.format(file))
    print('total train_data_list size is {}'.format(len(train_data_list)))
    random.shuffle(train_data_list)
    write_train_data(train_data_list)
