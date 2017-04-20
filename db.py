from pymongo import MongoClient


conn = MongoClient('localhost',27017)
db = conn.chat_log
group_log = db.group_log
person_log = db.person_log


class GroupLog(object):

    @classmethod
    def insert(cls,dic):
        return group_log.insert(dic)


class PersonLog(object):

    @classmethod
    def insert(cls,dic):
        return person_log.insert(dic)
