import jieba
from jieba import analyse
from db import *
import jieba.posseg as psg


def get_key_word(content):
    tfidf = analyse.extract_tags
    keywords = tfidf(content)
    return keywords


def get_all_word(content):
    fully_word = list(jieba.cut(content, cut_all=True))
    return fully_word


def get_noun_word(content):
    fully_word = psg.cut(content)
    term_word = []
    for word in fully_word:
        if word.flag.find('n') != -1:
            term_word.append(word.word)
    print(term_word)
    return term_word


def insert_conversition(conversition):
    for count in range(len(conversition)-1):
        dic = {'question': conversition[count],
               'answer': conversition[count+1]}
        if not Template.insert(dic):
            return 'fail'
    return 'success'


def batch_import_template():
    count = 0
    with open('corpus/template/xiaohuangji.conv', 'r') as file:
        conversition = []
        for line in file.readlines():
            line = line.strip()
            if line[0] == 'E':
                insert_conversition(conversition)
                conversition = []
            line = line[2:]
            conversition.append(line)
            count += 1
            print(count)
        insert_conversition(conversition)


if __name__ == "__main__":
    batch_import_template()
