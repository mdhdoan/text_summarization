import math, nltk, os, operator
from nltk.tag import pos_tag
from nltk.corpus import conll2000, stopwords, wordnet
from nltk.stem import WordNetLemmatizer, SnowballStemmer
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
wnl = WordNetLemmatizer()
sns = SnowballStemmer('english')
all_chunk_dict = {}
file_path = 'BBC News Summary/News Articles/'
np_grammar = '''
    NP CHUNK:   {<VB>?<JJ>*(<NN>|<NNS>)+}
                {<NNP>+}
'''

def chunk_print(doc_chunk_dict):
    sort_dict = {}
    np_list = list(doc_chunk_dict.keys())
    np_group = []
    for np_chunk in np_list:
        np_group.append(np_chunk.split('**'))
        for np in np_group:
            sort_dict[np_chunk] = [len(np)]
    for np, value in sort_dict.items():
        value.append(doc_chunk_dict[np][0])
    sorted_list = sorted(sort_dict.items(), key=operator.itemgetter(1))
    sorted_dict = dict(sorted_list)
    for np in sorted_dict.keys():
        print('np: ', np)
        print('  tfidf: ', doc_chunk_dict[np][0])
        print('  tf: ', doc_chunk_dict[np][1])
        print('  idf: ', doc_chunk_dict[np][2])
        print('  detail: ', doc_chunk_dict[np][3])

def idf_calc(doc_number, doc_chunk_dict):
    del_np_list = []
    for np, doc_list in doc_chunk_dict.items():
        doc_sum = len(doc_list)
        tf = 0.0
        for doc in doc_list:
            tf += doc[1]
        idf = math.log10(doc_number/doc_sum)
        # print(tf, idf)
        tfidf = tf*idf
        if idf == 0.0:
            del_np_list.append(np)
            doc_chunk_dict[np] = [tfidf, tf, idf, doc_list]
        else:
            doc_chunk_dict[np] = [tfidf, tf, idf, doc_list]
    # for np in del_np_list:
    #     del del_np_list[np]
    return del_np_list

def tuple_gathering(tuple_mix_list):
    result = set()
    for item in tuple_mix_list:
        if type(item) == tuple:
            result.add(item[0])
    return result


def np_chunking(word_tag_list):
    cp = nltk.RegexpParser(np_grammar)
    np_chunk = cp.parse(word_tag_list)
    np_chunk_dict = {}
    eng_stopwords = stopwords.words('english')
    for subtree in np_chunk.subtrees(filter = lambda t: t.label() == 'NP CHUNK'):
        chunk_list = [w for w in subtree if not w[0].lower() in eng_stopwords if w[0].isalpha()]
        if chunk_list == []:
            continue
        tuple_gathering(chunk_list)
        sw_list = []
        for w in subtree:
            if w[1].startswith('NN'):
                lw = wnl.lemmatize(w[0], 'n')
                sw_list.append(sns.stem(lw))
        # print(sw_list)
        key = '**'.join(term for term in sw_list)
        if key in np_chunk_dict:
            np_chunk_dict[key].append([tuple_gathering(chunk_list)])
        else:
            np_chunk_dict[key] = [tuple_gathering(chunk_list)]
    return np_chunk_dict


def np_chunk_build(doc_path_list, article, doc_chunk_dict):
    doc_id = article.split('.')[0]
    doc = open(doc_path_list, 'r')
    text = doc.readlines()
    sentence_list = []
    current_doc_chunk_dict = {}
    for line in text:
        sentence_list.extend(nltk.sent_tokenize(line))
    sent_id = 0
    for sentence in sentence_list:
        sent_id += 1
        word_list = nltk.word_tokenize(sentence)
        word_tag_list = pos_tag(word_list)
        np_chunk_dict = np_chunking(word_tag_list)
        #replacing original word here:
        for key, value in np_chunk_dict.items():
            chunk_freq = len(value)
            np_chunk_dict[key] = [doc_id, 1, [chunk_freq, sent_id]]
        if np_chunk_dict == []:
            continue
        for key, value in np_chunk_dict.items():
            if key in current_doc_chunk_dict.keys():
                cd_id = current_doc_chunk_dict[key][0]
                np_d_id = value[0]
                if np_d_id == cd_id:
                    current_doc_chunk_dict[key][1] += 1
                    current_doc_chunk_dict[key].append(value[2])
                else:
                    current_doc_chunk_dict[key].append(value)
            else:
                current_doc_chunk_dict[key] = value
    for key, value in current_doc_chunk_dict.items():
        if key in doc_chunk_dict.keys():
            doc_chunk_dict[key].append(value)
        else: 
            doc_chunk_dict[key] = [value]
    # print(current_doc_chunk_dict)


# Boost via length of np
def sent_tfidf_calc(chunk_list):
    tfidf_sum = 0.0
    for chunk in chunk_list:
        tfidf = chunk[1]
        np = chunk[0].split('**')
        boost = len(np)
        tfidf_sum += tfidf * (2 ** boost)
    return tfidf_sum


## sentence_pairing sets tfidf to be paired
def sentence_pairing(doc_path_list, article, doc_chunk_dict):
    doc = open(doc_path_list, 'r')
    text = doc.readlines()
    sentence_dict = {}
    sentence_list = []
    for line in text:
        sentence_line = nltk.sent_tokenize(line)
        if sentence_line != []:
            for sentence in sentence_line:
                sentence_list.append(sentence)
        else: 
            continue
    # print(sentence_list)
    sent_counter = 0
    for sentence in sentence_list:
        sent_counter += 1
        key = str(sentence)  
        sentence_dict[key] = sent_counter
    doc_chunk_holder = {}
    for key, values in doc_chunk_dict.items():
        for doc in values[3]:
            doc_id = doc[0]
            article_id = article.split('.')[0]
            if doc_id == article_id:
                s_detail = doc[2:]
                for _, sid in s_detail:
                    if sid in doc_chunk_holder.keys():
                        doc_chunk_holder[sid].append([key, values[0]])
                    else:
                        doc_chunk_holder[sid] = [[key, values[0]]]
    for sent, sid in sentence_dict.items():
        if sid in doc_chunk_holder.keys():
            tfidf_sum = sent_tfidf_calc(doc_chunk_holder[sid])
            sentence_dict[sent] = [tfidf_sum, doc_chunk_holder[sid]]
        else: 
            sentence_dict[sent] = [0]
    return sentence_dict


def rank_sentence(sentence_dict, top):
    sent_list = list(sentence_dict.keys())
    sort_dict = {}
    sent_group = []
    for sent in sent_list:
        sent_group.append(sent.split('**'))
        for np in sent_group:
            sort_dict[sent] = [len(np)]
    for np, value in sort_dict.items():
        value.append(float(sentence_dict[np][0])*float(value[0]))
    sorted_list = sorted(sort_dict.items(), key=operator.itemgetter(1), reverse=True)[:top]
    sorted_dict = dict(sorted_list)
    return sorted_dict


def write_summary(top_sent_rank, summary_type, article):
    summary_file = open(summary_path + summary_type + article, 'w')
    print('writing summaries for ', article)
    for sentence in top_sent_rank:
        write_sentence = sentence + '\n\n'
        summary_file.write(write_sentence)


def category_summary(summary_type):
    doc_path_list = []
    counter = 0
    article_list = os.listdir(file_path + summary_type)
    doc_chunk_dict = {}
    # article_list = ['014.txt']
    for article in article_list[:]:
        doc_path_list = (file_path + summary_type + article)
        counter += 1
        # print("Article #" + str(counter) + ': ' + article)
        np_chunk_build(doc_path_list, article, doc_chunk_dict)
    
    np_del_list = idf_calc(counter, doc_chunk_dict)
    # print('Appear everywhere: \n', np_del_list)
    # chunk_print(doc_chunk_dict)
    # print('calculated_idf')
    for key, values in doc_chunk_dict.items():
        if key in all_chunk_dict.keys():
            all_chunk_dict[key].append([summary_type[:-1], values])
        else:
            all_chunk_dict[key] = [summary_type[:-1], values]

    for article in article_list[:]:
        # print("Article: ", article)
        doc_path_list = file_path + summary_type + article
        sentence_chunk_pair_list = sentence_pairing(doc_path_list, article, doc_chunk_dict)
        # print('sentence_chunk_pair_list: \n', sentence_chunk_pair_list)
        T5_sent_ranked = rank_sentence(sentence_chunk_pair_list, 5)
        # print(T5_sent_ranked)
        write_summary(T5_sent_ranked, summary_type, article)


if __name__ == '__main__':
    categories = ['business/','entertainment/','politics/','sport/','tech/']
    summary_path = 'My Summaries/'
    for category in categories:
        category_summary(category)
    
