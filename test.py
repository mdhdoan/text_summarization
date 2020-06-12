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

def chunk_print(doc_chunk_list):
    for chunk in doc_chunk_list:
        for key, value in chunk.items():
            print('chunk: ', key)
            for doc_id in [value[1]]:
                print(' doc_id: ', doc_id)
                sent_detail = value[2]
                print('  og_sent: ',sent_detail[0], '\tsid: ', sent_detail[1])

def idf_calc(document_number):
    del_NP_list = []
    for NP, doc_list in doc_chunk_dict.items():
        doc_sum = 0
        for doc in doc_list:
            doc_sum += int(doc[1])
        idf = math.log10(document_number/doc_sum)
        if idf == 0.0:
            del_NP_list.append(NP)
        else:
            doc_chunk_dict[NP] = [idf, doc_list]
    return del_NP_list
    # for term in del_term:
    #     del doc_freq[NP]


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


# def sentence_counter(term, sentence):
#     for term in sentence: 


def doc_detail(document_path_list, article):
    doc_id = article.split('.')[0]
    # print(doc_id)
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
                    # print(doc_chunk_dict[key])
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
        
# business_articles_list = os.listdir('BBC News Summary/News Articles/business/')
# entertainment_articles_list = os.listdir('BBC News Sumtfidfary/News Articles/entertainment/')
# politics_articles_list = os.listdir('BBC News Summary/News Articles/politics/')
# sport_articles_list = os.listdir('BBC News Summary/News Articles/sport/')
tech_articles_list = os.listdir('BBC News Summary/News Articles/tech/')
document_path_list = []
counter = 0


# for article in business_articles_list:
#     document_path_list = 'BBC News Summary/News Articles/business/' + article
#     counter += 1
#     print("Article #" + str(counter) + ': ' + article)
#     doc_detail(document_path_list)
# # print("word_freq: \n ", word_freq, "\n")
# sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
# print('sorted_freq: \n', sorted_freq)
# sorted_freq = []

# document_path_list = []
# counter = 0
# for article in entertainment_articles_list:
#     document_path_list = 'BBC News Summary/News Articles/entertainment/' + article
#     counter += 1
#     # print("Article #" + str(counter) + ': ' + article)
#     doc_detail(document_path_list)
# # print("word_freq: \n ", word_freq, "\n")
# sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
# print('sorted_freq: \n', sorted_freq)
# sorted_freq = []

# document_path_list = []
# counter = 0
# for article in politics_articles_list:
#     document_path_list = 'BBC News Summary/News Articles/politics/' + article
#     counter += 1
#     # print("Article #" + str(cbreakounter) + ': ' + article)
#     doc_detail(document_path_list)
# # print("word_freq: \n ", word_freq, "\n")
# sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
# print('sorted_freq: \n', sorted_freq)
# sorted_freq = []

# document_path_list = []
# counter = 0
# for article in sport_articles_list:
#     document_path_list = 'BBC News Summary/News Articles/sport/' + article
#     counter += 1
#     # print("Article #" + str(counter) + ': ' + article)
#     doc_detail(document_path_list)
# # print("word_freq: \n ", word_freq, "\n")
# sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
# print('sorted_freq: \n', sorted_freq)
# sorted_freq = []

document_path_list = []
counter = 0
for article in tech_articles_list[:5]:
    document_path_list = ('BBC News Summary/News Articles/tech/' + article)
    # summary_path_list = ('BBC News Summary/Summaries/tech/' + article)
    counter += 1
    print("Article #" + str(counter) + ': ' + article)
    doc_detail(document_path_list, article)
    # print("doc_chunk_dict: ", doc_chunk_dict)
    # print("Sum Article doc_freq = {}
# print("doc_chunk_dict: \n", doc_chunk_dict)
NP_del_list = idf_calc(counter)
print('Appear everywhere: \n', NP_del_list)
# print("doc_chunk_dict: \n", doc_chunk_dict)

# sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
# print('sorted_freq: \n', sorted_freq[:5])