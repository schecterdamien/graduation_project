from jieba import analyse
from db import *


def get_key_word(content):
    tfidf = analyse.extract_tags
    keywords = tfidf(content)
    return keywords


def insert_conversition(conversition):
    for count in range(len(conversition)-1):
        dic = {'question': conversition[count],
               'answer': conversition[count+1]}
        Template.insert(dic)
    print('插入成功')


def batch_import_template():
    count = 0
    with open('corpus/tempalte/fanzxl.conv', 'r') as file:
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
    batch_import()