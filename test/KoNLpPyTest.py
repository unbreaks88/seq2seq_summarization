from gensim.models.word2vec import Word2Vec
import csv
from konlpy.tag import Twitter

twitter = Twitter()


def tokenize(doc):
    return 111

def tokenizeNews(reader, writer):
    i = 0
    for line in reader:
        i +=1
        print(i)
        # print(line)111
        title = tokenize(twitter.morphs(line[1]))
        contents = tokenize(twitter.morphs(line[2]))
        summary = tokenize(twitter.morphs(line[3]))

        # title = ','.join(twitter.morphs(line[1])).strip()
        # contents = ','.join(twitter.morphs(line[2])).strip()
        # summary = ','.join(twitter.morphs(line[3])).strip()
        list = ["문화", title, contents, summary]
        print(list)

        model = Word2Vec(list)

        writer.writerow(list)

if __name__ == '__main__':
    file_reader = open('/Users/unbreaks/git/seq2seq_summarization/data/culture/201801_culture.csv', mode='r',
                       encoding='utf-8')
    reader = csv.reader(file_reader, delimiter='\t')

    file_write = open('/Users/unbreaks/git/seq2seq_summarization/data/culture/tokenized/201801_culture.csv', mode='w',
                      encoding='utf-8')
    writer = csv.writer(file_write, delimiter='\t')



    tokenizeNews(reader, writer)

    file_reader.close()
    file_write.close()
