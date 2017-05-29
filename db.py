from pymongo import MongoClient
import traceback
from utils import get_noun_word, KeyWordHandle
import redis
from bson.objectid import ObjectId

mongo_conn = MongoClient('localhost', 27017)
mongo_db = mongo_conn.chat_log

group_log = mongo_db.group_log
person_log = mongo_db.person_log
template = mongo_db.template

angry = mongo_db.angry
depressed = mongo_db.depressed
disgust = mongo_db.disgust
happy = mongo_db.happy

re_conn = redis.Redis(host='localhost', port=6379)

DEFAULT_TEMPLATE = 'corpus/template/xiaohuangji.conv'


class GroupLog(object):

    @classmethod
    def insert(cls, dic):
        return group_log.insert(dic)


class PersonLog(object):

    @classmethod
    def insert(cls, dic):
        return person_log.insert(dic)


class EmotionBase(object):
    emotion = None

    @classmethod
    def insert(cls, answer):
        none_word = get_noun_word(answer)
        dict = {'answer': answer, 'term_word': none_word}
        return cls.emotion.insert(dict)

    @classmethod
    def get(cls, words):
        return list(cls.emotion.find({'term_word': {'$in': words}}))


class Angry(EmotionBase):
    emotion = angry


class Depressed(EmotionBase):
    emotion = depressed


class Disgust(EmotionBase):
    emotion = disgust


class Happy(EmotionBase):
    emotion = happy


class Template(object):

    #两个插入需要加入异常捕获
    @classmethod
    def insert(cls, dic, key_word_hander):
        key_words = key_word_hander.get_key_word_list(dic['question'])
        dic['key_words'] = key_words
        try:
            mongo_id = str(template.insert(dic))
            for key_word in key_words:
                re_conn.rpush(key_word, mongo_id)
        except Exception:
            print(dic)
            traceback.print_exc()
            return 'fail'
        if mongo_id:
            return 'success'

    @classmethod
    def get_candidate_set(cls, key_words):
        candidate_dict = {}
        max_num = 0
        max_set = set()
        print('——————————————筛选候选集——————————————————————')
        print(key_words)
        for key_word in key_words:
            list_count = re_conn.llen(key_word)
            # print('%s关键字有%d个qa对' % (key_word, list_count))
            for index in range(list_count):
                obj_id = re_conn.lindex(key_word, index)
                obj_id = obj_id.decode('ascii')
                if candidate_dict.get(obj_id):
                    candidate_dict[obj_id] += 1
                else:
                    candidate_dict[obj_id] = 1
                if candidate_dict[obj_id] > max_num:
                    max_num = candidate_dict[obj_id]
            # print('经过%s关键字，最大值为：%d，列表为：' % (key_word, max_num))
            # print(candidate_dict)
        # print('最终得到最大值为：%d ,列表为:' % (max_num))
        # print(candidate_dict)
        for obj_id, num in candidate_dict.items():
            if num == max_num:
                max_set.add(obj_id)
        print('最终筛选集为:')
        print(max_set)
        return max_set

    @classmethod
    def get_by_id(cls, obj_id):
        return template.find_one({"_id": ObjectId(obj_id)})

    @classmethod
    def get_all(cls):
        return template.find().count()


class TemplateImportHandle():

    def __init__(self):
        self.key_word_hander = KeyWordHandle()

    def insert_conversition(self, conversition):
        for count in range(len(conversition)-1):
            dic = {'question': conversition[count].replace('.', ''),
                   'answer': conversition[count+1]}
            if not Template.insert(dic, self.key_word_hander):
                return 'fail'
        return 'success'

    def batch_import_template(self):
        count = 0
        with open(DEFAULT_TEMPLATE, 'r') as file:
            conversition = []
            for line in file.readlines():
                line = line.strip()
                if line[0] == 'E':
                    self.insert_conversition(conversition)
                    conversition = []
                else:
                    line = line[2:]
                    conversition.append(line)
                    count += 1
                    print(count)

    # def syn_from_mongo_to_redis(self):

if __name__ == '__main__':
    templateImportHandle = TemplateImportHandle()
    templateImportHandle.batch_import_template()