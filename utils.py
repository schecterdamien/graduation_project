import jieba
from jieba import analyse
import jieba.posseg as psg


DEFAULT_IDF = 'corpus/idf.txt'
DEFAULT_STOPWORD = 'corpus/stop_words.txt'


class IDFLoader(object):

    def __init__(self, idf_path=DEFAULT_IDF):
        self.path = idf_path
        self.idf_freq = {}
        self.median_idf = 0.0
        if idf_path:
            self.init_idf(idf_path)

    def init_idf(self, new_idf_path):
        self.path = new_idf_path
        content = open(new_idf_path, 'rb').read().decode('utf-8')
        self.idf_freq = {}
        for line in content.splitlines():
            word, freq = line.strip().split(' ')
            self.idf_freq[word] = float(freq)
        self.median_idf = sorted(
            self.idf_freq.values())[len(self.idf_freq) // 2]

    def get_idf(self):
        return self.idf_freq, self.median_idf


class StopWordLoader(object):

    def __init__(self, stop_word_path=DEFAULT_STOPWORD):
        self.path = stop_word_path
        self.stop_word_list = []
        if stop_word_path:
            self.init_stop_word_list(stop_word_path)

    def init_stop_word_list(self, new_idf_path):
        self.path = new_idf_path
        content = open(new_idf_path, 'rb').read().decode('utf-8')
        for line in content.splitlines():
            line = line.strip()
            self.stop_word_list.append(line)


class KeyWordHandle(object):

    def __init__(self, idf_path=DEFAULT_IDF, stop_word_path=DEFAULT_STOPWORD):
        self.idf_loader = IDFLoader(idf_path)
        self.stop_word_loader = StopWordLoader(stop_word_path)
        self.stop_word_list = self.stop_word_loader.stop_word_list

    def get_key_word_list(self, content, top_num=20):
        idf_freq, median_idf = self.idf_loader.get_idf()
        word_freq = {}
        words = jieba.cut(content)
        for word in words:
            if word in self.stop_word_list:
                continue
            word_freq[word] = word_freq.get(word, 0.0) + 1.0
        total = sum(word_freq.values())
        for word in word_freq:
            word_freq[word] *= idf_freq.get(word, median_idf) / total
        result = sorted(word_freq, key=word_freq.__getitem__, reverse=True)
        key_word_list = result[:top_num]
        result = {}
        for word in word_freq:
            if word in key_word_list:
                result[word] = word_freq[word]
        return result


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


if __name__ == "__main__":
    key_word_handle = KeyWordHandle()
    print(key_word_handle.get_key_word_list('你的名字叫什么'))