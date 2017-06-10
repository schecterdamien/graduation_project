from utils import *
from db import Template, Angry, Depressed, Disgust, Happy
from emotion_classifier import emotion_recognition


emotion_map = {'angry': Angry,
               'depressed': Depressed,
               'disgust': Disgust,
               'happy': Happy}


def common_response(content):
    print('问句原文： {}'.format(content))
    key_word_hander = KeyWordHandle()
    key_words = key_word_hander.get_key_word_list(content)
    candidate_dict = Template.get_candidate_set(list(key_words))
    matching = {}
    if not candidate_dict:
        return 'no result'
    for obj_id in candidate_dict:
        print('-----------计算相似度---------模版id为：%s -------------' % obj_id)
        template = Template.get_by_id(obj_id)
        similarity = similarity_calculate(question_keys=key_words, template_keys=template['key_words'])
        print('计算得到 %s 模版和问句相似度为 %s' % (obj_id, similarity))
        matching[obj_id] = similarity
    print('-------------------------------最终匹配结果-------------------------------')
    best_match_id = max(matching.items(), key=lambda item: item[1])[0]
    print('最匹配模版的id为：{}    相似度为：{}'.format(best_match_id, matching[best_match_id]))
    best_match_template = Template.get_by_id(best_match_id)
    print('最匹配模版中的问题为：{}    答案为：{}'.format(best_match_template['question'], best_match_template['answer']))
    return best_match_template['answer']


def similarity_calculate(question_keys, template_keys):
    question_keys_set = set(question_keys)
    template_keys_set = set(template_keys)
    keys_set = question_keys_set | template_keys_set
    print('用户问句关键字集合为：{}'.format(question_keys_set))
    print('待计算模版关键字集合为：{}'.format(template_keys_set))
    print('关键字集合并集为：{}'.format(keys_set))
    qusetion_array = []
    template_array = []
    for key_word in keys_set:
            qusetion_array.append(question_keys.get(key_word, 0.0))
            template_array.append(template_keys.get(key_word, 0.0))
    print('用户问句词向量为：{}'.format(qusetion_array))
    print('待计算模版词向量为：{}'.format(template_array))
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for i in range(len(keys_set)):
        result1 += qusetion_array[i] * template_array[i]
        result2 += qusetion_array[i] ** 2
        result3 += template_array[i] ** 2
    similarity = result1 / (result2 * result3) ** 0.5
    return similarity


def emotion_recognize(content):
    answer_maps = {'angry': '别生气了，生气对身体不好',
                   'happy': '小Z也很高兴啊,愿你天天都可以这么开心',
                   'depressed': '假如生活欺骗了你，今天就多吃点'}
    emotion = emotion_recognition(content)
    print(emotion)
    if emotion == 'fail':
        answer = '小Z没有识别到您的情感'
        return answer
    none_words = get_noun_word(content)
    mongo_obj = emotion_map[emotion]
    answer = mongo_obj.get(none_words)
    if not answer:
        answer = answer_maps[emotion]
    print(answer)
    return answer


if __name__ == '__main__':
    pass