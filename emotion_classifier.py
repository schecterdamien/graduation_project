import jieba
import pickle
import math


def init_emotion_words_set(path):
    emotion_words_set = set()
    with open(path, 'r') as file:
        for word in file.readlines():
            word = word.rstrip('\n')
            emotion_words_set.add(word)
    # print('情感词典长度：%s' % len(emotion_words_set))
    return emotion_words_set


def init_train_sentences_list(path):
    train_sentences_list = []
    with open(path, 'r') as file:
        for line in file.readlines():
            if not line.isspace():
                line = line.strip()
                train_sentences_list.append(line)
    print('训练集句子数：%s' % len(train_sentences_list))
    return train_sentences_list


def get_words_frequency(emotion_words_set, train_sentences_list):
    words_frequency_dict = dict([(word, 0) for word in emotion_words_set])
    train_words_list = [list(set(jieba.cut(sentence))) for sentence in train_sentences_list]
    print('训练集分词完毕')
    for sentence_seg in train_words_list:
        for word in sentence_seg:
            if word in words_frequency_dict:
                words_frequency_dict[word] = words_frequency_dict.get(word, 0) + 1
    print('训练集统计完毕')
    return words_frequency_dict


def get_words_rate(words_frequency_dict, sum):
    words_rate_dict = dict([(key, (value + 1) / (sum + 2)) for key, value in words_frequency_dict.items()])
    print('训练集学习完毕')
    return words_rate_dict


def training():
    emotion_words_set = init_emotion_words_set('corpus/NTUSD_vocabulary_simplified.txt')
    angry_train_sentences_list = init_train_sentences_list('corpus/emotion/train/angry.txt')
    depressed_train_sentences_list = init_train_sentences_list('corpus/emotion/train/depressed.txt')
    happy_train_sentences_list = init_train_sentences_list('corpus/emotion/train/happy.txt')

    angry_words_frequency_dict = get_words_frequency(emotion_words_set, angry_train_sentences_list)
    depressed_words_frequency_dict = get_words_frequency(emotion_words_set, depressed_train_sentences_list)
    happy_words_frequency_dict = get_words_frequency(emotion_words_set, happy_train_sentences_list)

    angry_words_rate_dict = get_words_rate(angry_words_frequency_dict, len(angry_train_sentences_list))
    depressed_words_rate_dict = get_words_rate(depressed_words_frequency_dict, len(depressed_train_sentences_list))
    happy_words_rate_dict = get_words_rate(happy_words_frequency_dict, len(happy_train_sentences_list))
    dump_train_result(angry_words_rate_dict, depressed_words_rate_dict, happy_words_rate_dict)

    return 'ok'


def dump_train_result(angry_words_rate_dict, depressed_words_rate_dict, happy_words_rate_dict):
    with open('corpus/emotion/emotion_train_result', "wb") as file:
        pickle.dump(angry_words_rate_dict, file)
        pickle.dump(depressed_words_rate_dict, file)
        pickle.dump(happy_words_rate_dict, file)
    return 'success'


def load_train_result():
    with open('corpus/emotion/emotion_train_result', "rb") as file:
        angry_words_rate_dict = pickle.load(file)
        depressed_words_rate_dict = pickle.load(file)
        happy_words_rate_dict = pickle.load(file)
        emotion_words_rate_dict = {'angry_words_rate_dict': angry_words_rate_dict,
                                   'depressed_words_rate_dict': depressed_words_rate_dict,
                                   'happy_words_rate_dict': happy_words_rate_dict
                                   }
    return emotion_words_rate_dict


def _emotion_recognition(sentence, emotion_words_rate_dict):
    emotion_words_set = init_emotion_words_set('corpus/NTUSD_vocabulary_simplified.txt')
    words = []
    for word in jieba.cut(sentence, cut_all=True):
        # print(word)
        if word in emotion_words_set:
            words.append(word)
    print(words)
    if not words:
        return 'fail'
    angry_likelihood_list = []
    depressed_likelihood_list = []
    happy_likelihood_list = []
    for word in emotion_words_set:
        if word in words:
            angry_likelihood_list.append(emotion_words_rate_dict['angry_words_rate_dict'].get(word))
            depressed_likelihood_list.append(emotion_words_rate_dict['depressed_words_rate_dict'].get(word))
            happy_likelihood_list.append(emotion_words_rate_dict['happy_words_rate_dict'].get(word))
        else:
            angry_likelihood_list.append(1-emotion_words_rate_dict['angry_words_rate_dict'].get(word))
            depressed_likelihood_list.append(1-emotion_words_rate_dict['depressed_words_rate_dict'].get(word))
            happy_likelihood_list.append(1-emotion_words_rate_dict['happy_words_rate_dict'].get(word))

    # print(words)
    angry_likelihood = sum(map(lambda x: math.log(x), angry_likelihood_list))
    depressed_likelihood = sum(map(lambda x: math.log(x), depressed_likelihood_list))
    happy_likelihood = sum(map(lambda x: math.log(x), happy_likelihood_list))
    # print('angry_likelihood: %s ' % angry_likelihood)
    # print('depressed_likelihood: %s ' % depressed_likelihood)
    # print('happy_likelihood: %s ' % happy_likelihood)
    result_map = {'angry': angry_likelihood,
                  'depressed': depressed_likelihood,
                  'happy': happy_likelihood}

    result = max(result_map.items(), key=lambda item: item[1])[0]
    # print(result)
    return result


def emotion_recognition(sentence):
    emotion_words_rate_dict = load_train_result()
    result = _emotion_recognition(sentence, emotion_words_rate_dict)
    return result


def get_train_precision():
    angry_test_sentences_list = init_train_sentences_list('corpus/emotion/test/angry.txt')
    depressed_test_sentences_list = init_train_sentences_list('corpus/emotion/test/depressed.txt')
    happy_test_sentences_list = init_train_sentences_list('corpus/emotion/test/happy.txt')
    angry_test_result = 0
    depressed_test_result = 0
    happy_test_result = 0
    i = 0
    emotion_words_rate_dict = load_train_result()
    for sentence in angry_test_sentences_list:
        result = _emotion_recognition(sentence, emotion_words_rate_dict)
        i += 1
        print(i)
        if result == 'angry':
            angry_test_result += 1
    i = 0
    print('anrgy_test')
    for sentence in depressed_test_sentences_list:
        result = _emotion_recognition(sentence, emotion_words_rate_dict)
        i += 1
        print(i)
        if result == 'depressed':
            depressed_test_result += 1
    i = 0
    for sentence in happy_test_sentences_list:
        result = _emotion_recognition(sentence, emotion_words_rate_dict)
        i += 1
        print(i)
        if result == 'happy':
            happy_test_result += 1
    print('happy_test')
    print(angry_test_result, depressed_test_result, happy_test_result)

if __name__ == '__main__':
    # emotion_words_set = init_emotion_words_set('corpus/NTUSD_vocabulary_simplified.txt')
    training()
    # get_train_precision()
