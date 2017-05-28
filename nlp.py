from utils import *
from db import Template, Angry, Depressed, Disgust, Happy
from emotion_classifier import emotion_recognition


emotion_map = {'angry': Angry,
               'depressed': Depressed,
               'disgust': Disgust,
               'happy': Happy}


def common_response(content):
    key_word_hander = KeyWordHandle()
    key_words = key_word_hander.get_key_word_list(content)
    candidate_dict = Template.get_candidate_set(list(key_words))
    matching = {}
    if not candidate_dict:
        return 'no result'
    for obj_id in candidate_dict:
        print('计算相似度------模版id为：%s ' % obj_id)
        template = Template.get_by_id(obj_id)
        similarity = similarity_calculate(question_keys=key_words, template_keys=template['key_words'])
        print('%s 模版相似度为 %s' % (obj_id, similarity))
        matching[obj_id] = similarity
    best_match_id = max(matching.items(), key=lambda item: item[1])[0]
    print(best_match_id)
    best_match_template = Template.get_by_id(best_match_id)
    return best_match_template['answer']


def similarity_calculate(question_keys, template_keys):
    question_keys_set = set(question_keys)
    template_keys_set = set(template_keys)
    keys_set = question_keys_set | template_keys_set
    print('共有的关键字集合为：')
    print(keys_set)
    qusetion_array = []
    template_array = []
    for key_word in keys_set:
            qusetion_array.append(question_keys.get(key_word, 0.0))
            template_array.append(template_keys.get(key_word, 0.0))
    print('待匹配向量为：')
    print(qusetion_array)
    print('模版向量为：')
    print(template_array)
    result1 = 0.0
    result2 = 0.0
    result3 = 0.0
    for i in range(len(keys_set)):
        result1 += qusetion_array[i] * template_array[i]
        result2 += qusetion_array[i] ** 2
        result3 += template_array[i] ** 2
    similarity = result1 / (result2 * result3) ** 0.5
    print('result1 = %s, result2 = %s result3 = %s similarity = %s' % (result1, result2, result3, similarity))
    return similarity


def emotion_recognize(content):
    answer_maps = {'angry': '别生气了，生气对身体不好',
                   'happy': '小Z也很高兴啊,愿你天天都可以这么开心',
                   'depressed': '假如生活欺骗了你，今天就多吃点',
                   'disgust': '那个……我不是针对谁，我想说……在做的各位……都是……垃圾'}
    emotion = emotion_recognition(content)
    print(emotion)
    if not emotion:
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