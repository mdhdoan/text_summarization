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
doc_chunk_dict = {}
NP_grammar = '''
    NP CHUNK:   {<VB>?<JJ>*(<NN>|<NNS>)+}
                {<NNP>+}
'''

def chunk_print(doc_chunk_dict):
    sort_dict = {}
    NP_list = list(doc_chunk_dict.keys())
    NP_group = []
    for NP_chunk in NP_list:
        NP_group.append(NP_chunk.split('**'))
        for NP in NP_group:
            sort_dict[NP_chunk] = [len(NP)]
    for NP, value in sort_dict.items():
        value.append(doc_chunk_dict[NP][0])
    sorted_list = sorted(sort_dict.items(), key=operator.itemgetter(1))
    sorted_dict = dict(sorted_list)
    for NP in sorted_dict.keys():
        print('NP: ', NP)
        print('  tfidf: ', doc_chunk_dict[NP][0])
        print('  tf: ', doc_chunk_dict[NP][1])
        print('  idf: ', doc_chunk_dict[NP][2])
        print('  detail: ', doc_chunk_dict[NP][3])

def idf_calc(document_number):
    del_NP_list = []
    for NP, doc_list in doc_chunk_dict.items():
        doc_sum = len(doc_list)
        tf = 0.0
        for doc in doc_list:
            tf += doc[1]
        idf = math.log10(document_number/doc_sum)
        # print(tf, idf)
        tfidf = tf*idf
        if idf == 0.0:
            del_NP_list.append(NP)
            doc_chunk_dict[NP] = [tfidf, tf, idf, doc_list]
        else:
            doc_chunk_dict[NP] = [tfidf, tf, idf, doc_list]
    # for NP in del_NP_list:
    #     del del_NP_list[NP]
    return del_NP_list

def tuple_gathering(tuple_mix_list):
    result = set()
    for item in tuple_mix_list:
        if type(item) == tuple:
            result.add(item[0])
    return result


def NP_chunking(word_tag_list):
    cp = nltk.RegexpParser(NP_grammar)
    NP_chunk = cp.parse(word_tag_list)
    NP_chunk_dict = {}
    eng_stopwords = stopwords.words('english')
    for subtree in NP_chunk.subtrees(filter = lambda t: t.label() == 'NP CHUNK'):
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
        if key in NP_chunk_dict:
            NP_chunk_dict[key].append([tuple_gathering(chunk_list)])
        else:
            NP_chunk_dict[key] = [tuple_gathering(chunk_list)]
    return NP_chunk_dict


def NP_chunk_build(document_path_list, article):
    doc_id = article.split('.')[0]
    document = open(document_path_list, 'r')
    text = document.readlines()
    sentence_list = []
    current_doc_chunk_dict = {}
    for line in text:
        sentence_list.extend(nltk.sent_tokenize(line))
    sent_id = 0
    for sentence in sentence_list:
        sent_id += 1
        word_list = nltk.word_tokenize(sentence)
        word_tag_list = pos_tag(word_list)
        NP_chunk_dict = NP_chunking(word_tag_list)
        #replacing original word here:
        for key, value in NP_chunk_dict.items():
            chunk_freq = len(value)
            NP_chunk_dict[key] = [doc_id, 1, [chunk_freq, sent_id]]
        if NP_chunk_dict == []:
            continue
        for key, value in NP_chunk_dict.items():
            if key in current_doc_chunk_dict.keys():
                cd_id = current_doc_chunk_dict[key][0]
                NP_d_id = value[0]
                if NP_d_id == cd_id:
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
        
# def doc_examine(doc_id):
#     for NP, values in doc_chunk_dict.items():

    

if __name__ == '__main__':
    business_articles_list = os.listdir('BBC News Summary/News Articles/business/')
    entertainment_articles_list = os.listdir('BBC News Summary/News Articles/entertainment/')
    politics_articles_list = os.listdir('BBC News Summary/News Articles/politics/')
    sport_articles_list = os.listdir('BBC News Summary/News Articles/sport/')
    tech_articles_list = os.listdir('BBC News Summary/News Articles/tech/')
    document_path_list = []
    counter = 0


    # document_path_list = []
    # counter = 0
    # for article in business_articles_list[:]:
    #     document_path_list = ('BBC News Summary/News Articles/business/' + article)
    #     # summary_path_list = ('BBC News Summary/Summaries/business/' + article)
    #     counter += 1
    #     print("Article #" + str(counter) + ': ' + article)
    #     NP_chunk_build(document_path_list, article)
    # NP_del_list = idf_calc(counter)
    # print('Appear everywhere: \n', NP_del_list)
    # chunk_print(doc_chunk_dict)

    # document_path_list = []
    # counter = 0
    # for article in entertainment_articles_list[:]:
    #     document_path_list = ('BBC News Summary/News Articles/entertainment/' + article)
    #     # summary_path_list = ('BBC News Summary/Summaries/entertainment/' + article)
    #     counter += 1
    #     print("Article #" + str(counter) + ': ' + article)
    #     NP_chunk_build(document_path_list, article)
    # NP_del_list = idf_calc(counter)
    # print('Appear everywhere: \n', NP_del_list)
    # chunk_print(doc_chunk_dict)

    # document_path_list = []
    # counter = 0
    # for article in politics_articles_list[:]:
    #     document_path_list = ('BBC News Summary/News Articles/politics/' + article)
    #     # summary_path_list = ('BBC News Summary/Summaries/politics/' + article)
    #     counter += 1
    #     print("Article #" + str(counter) + ': ' + article)
    #     NP_chunk_build(document_path_list, article)
    # NP_del_list = idf_calc(counter)
    # print('Appear everywhere: \n', NP_del_list)
    # chunk_print(doc_chunk_dict)

    # document_path_list = []
    # counter = 0
    # for article in sport_articles_list[:]:
    #     document_path_list = ('BBC News Summary/News Articles/sport/' + article)
    #     # summary_path_list = ('BBC News Summary/Summaries/sport/' + article)
    #     counter += 1
    #     print("Article #" + str(counter) + ': ' + article)
    #     NP_chunk_build(document_path_list, article)
    # NP_del_list = idf_calc(counter)
    # print('Appear everywhere: \n', NP_del_list)
    # chunk_print(doc_chunk_dict)

    document_path_list = []
    counter = 0
    for article in tech_articles_list[:]:
        document_path_list = ('BBC News Summary/News Articles/tech/' + article)
        # summary_path_list = ('BBC News Summary/Summaries/tech/' + article)
        counter += 1
        print("Article #" + str(counter) + ': ' + article)
        NP_chunk_build(document_path_list, article)
    NP_del_list = idf_calc(counter)
    print('Appear everywhere: \n', NP_del_list)
    chunk_print(doc_chunk_dict)

    # sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
    # print('sorted_freq: \n', sorted_freq[:5])