import jieba
import pickle
import math


def init_emotion_words_set(path):
    emotion_words_set = set()
    with open(path, 'r') as file:
        for word in file.readlines():
            word = word.rstrip('\n')
            emotion_words_set.add(word)
    print('情感词典长度：%s' % len(emotion_words_set))
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
    angry_train_sentences_list = init_train_sentences_list('corpus/emotion/angry.txt')
    depressed_train_sentences_list = init_train_sentences_list('corpus/emotion/depressed.txt')
    disgust_train_sentences_list = init_train_sentences_list('corpus/emotion/disgust.txt')
    happy_train_sentences_list = init_train_sentences_list('corpus/emotion/happy.txt')

    angry_words_frequency_dict = get_words_frequency(emotion_words_set, angry_train_sentences_list)
    depressed_words_frequency_dict = get_words_frequency(emotion_words_set, depressed_train_sentences_list)
    disgust_words_frequency_dict = get_words_frequency(emotion_words_set, disgust_train_sentences_list)
    happy_words_frequency_dict = get_words_frequency(emotion_words_set, happy_train_sentences_list)

    angry_words_rate_dict = get_words_rate(angry_words_frequency_dict, len(angry_train_sentences_list))
    depressed_words_rate_dict = get_words_rate(depressed_words_frequency_dict, len(depressed_train_sentences_list))
    disgust_words_rate_dict = get_words_rate(disgust_words_frequency_dict, len(disgust_train_sentences_list))
    happy_words_rate_dict = get_words_rate(happy_words_frequency_dict, len(happy_train_sentences_list))
    dump_train_result(angry_words_rate_dict, depressed_words_rate_dict, disgust_words_rate_dict, happy_words_rate_dict)

    return 'ok'


def dump_train_result(angry_words_rate_dict, depressed_words_rate_dict, disgust_words_rate_dict, happy_words_rate_dict):
    with open('emotion_train_result', "wb") as file:
        pickle.dump(angry_words_rate_dict, file)
        pickle.dump(depressed_words_rate_dict, file)
        pickle.dump(disgust_words_rate_dict, file)
        pickle.dump(happy_words_rate_dict, file)
    return 'emotion_train_result'


def load_train_result():
    with open('emotion_train_result', "rb") as file:
        angry_words_rate_dict = pickle.load(file)
        depressed_words_rate_dict = pickle.load(file)
        disgust_words_rate_dict = pickle.load(file)
        happy_words_rate_dict = pickle.load(file)
    return angry_words_rate_dict, depressed_words_rate_dict, disgust_words_rate_dict, happy_words_rate_dict


def emotion_recognition(sentence):
    emotion_words_set = init_emotion_words_set('corpus/NTUSD_vocabulary_simplified.txt')
    words = []
    for word in jieba.cut(sentence, cut_all=True):
        print(word)
        if word in emotion_words_set:
            words.append(word)
        else:
            print('词典没有这个词')
    angry_words_rate_dict, depressed_words_rate_dict, disgust_words_rate_dict, happy_words_rate_dict = load_train_result()

    angry_likelihood_list = [1 - angry_words_rate_dict.get(word) if word not in words else angry_words_rate_dict.get(word) for word in
                             emotion_words_set]
    depressed_likelihood_list = [1 - depressed_words_rate_dict.get(word) if word not in words else depressed_words_rate_dict.get(word) for word in
                                 emotion_words_set]
    disgust_likelihood_list = [1 - disgust_words_rate_dict.get(word) if word not in words else disgust_words_rate_dict.get(word) for word in
                               emotion_words_set]
    happy_likelihood_list = [1 - happy_words_rate_dict.get(word) if word not in words else happy_words_rate_dict.get(word) for word in
                             emotion_words_set]
    print(words)
    angry_likelihood = sum(map(lambda x: math.log(x), angry_likelihood_list))
    depressed_likelihood = sum(map(lambda x: math.log(x), depressed_likelihood_list))
    disgust_likelihood = sum(map(lambda x: math.log(x), disgust_likelihood_list))
    happy_likelihood = sum(map(lambda x: math.log(x), happy_likelihood_list))
    print('angry_likelihood: %s ' % angry_likelihood)
    print('depressed_likelihood: %s ' % depressed_likelihood)
    print('disgust_likelihood: %s ' % disgust_likelihood)
    print('happy_likelihood: %s ' % happy_likelihood)
    result_map = {'angry': angry_likelihood,
                  'depressed': depressed_likelihood,
                  'disgust': disgust_likelihood,
                  'happy': happy_likelihood}

    result = max(result_map.items(), key=lambda item: item[1])[0]
    print(result)
    return result


if __name__ == '__main__':
    # emotion_words_set = init_emotion_words_set('corpus/NTUSD_vocabulary_simplified.txt')
    emotion_recognition('不高兴')
    # training()
    # generate_corpus()
