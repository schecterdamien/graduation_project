from utils import get_key_word
from db import Template


def response(content):
    key_words = get_key_word(content)
    candidate_dict = Template.get_candidate_set(key_words)
    matching = {}
    if not candidate_dict:
        return '无匹配模版'
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
        if key_word in question_keys_set:
            qusetion_array.append(1)
        else:
            qusetion_array.append(0)
        if key_word in template_keys_set:
            template_array.append(1)
        else:
            template_array.append(0)
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


if __name__ == '__main__':
    pass