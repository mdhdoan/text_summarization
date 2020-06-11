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
doc_freq = {}

NP_grammar = '''
    NP CHUNK:   {<VB>?<JJ>*(<NN>|<NNS>)+}
                {<NNP>+}
'''

def idf_calc(document_number):
    del_term = []
    for term in doc_freq:
        idf = math.log10(document_number/doc_freq[term][1])
        if idf == 0.0:
            print(term)
            del_term.append(term)
        else:
            doc_freq[term].append(idf)
    for term in del_term:
        del doc_freq[term]


def tuple_gathering(tuple_mix_list):
    result = set()
    for item in tuple_mix_list:
        if type(item) == tuple:
            result.add(item[0])
    return result


def NP_chunking(word_tag_list):
    cp = nltk.RegexpParser(NP_grammar)
    NP_chunk = cp.parse(word_tag_list)
    NP_chunk_list = []
    # Adding words to stopwords:
    eng_stopwords = stopwords.words('english')
    for subtree in NP_chunk.subtrees(filter = lambda t: t.label() == 'NP CHUNK'):
        chunk_list = [w for w in subtree if not w[0].lower() in eng_stopwords if w[0].isalpha()]
        if chunk_list == []:
            continue
        pair = [tuple_gathering(chunk_list), []]
        for w in subtree:
            if w[1].startswith('NN'):
                lw = wnl.lemmatize(w[0], 'n')
                sw = sns.stem(lw)
                pair[1].append(sw)
        NP_chunk_list.append(pair)
    return NP_chunk_list


def doc_detail(document_path_list):
    document = open(document_path_list, 'r')
    term_freq = {}
    text = document.readlines()
    sentence_list = []
    doc_chunk_list = []
    for line in text:
        sentence_list.extend(nltk.sent_tokenize(line))
    sent_counter = 0
    for sentence in sentence_list:
        sent_counter += 1
        word_list = nltk.word_tokenize(sentence)
        # word_stop_list = [word for word in word_list if not word.lower() in eng_stopwords]
        word_tag_list = pos_tag(word_list)#[word for word in word_stop_list if word.isalpha()]
        # print(word_tag_list)
        NP_chunk_list = NP_chunking(word_tag_list)
        if NP_chunk_list == []:
            continue
        NP_chunk_list.append(sent_counter)
        doc_chunk_list.append(NP_chunk_list)
        # for word, tag in NP_chunk_list:
        #     if tag.startswith('JJ'):
        #         lemmatized_word = wnl.lemmatize(word, 'a')
        #     elif tag.startswith('VB'):
        #         lemmatized_word = wnl.lemmatize(word, 'v')
        #     elif tag.startswith('NN'):
        #         lemmatized_word = wnl.lemmatize(word, 'n')
        #     else:
        #         lemmatized_word = wnl.lemmatize(word)
            
        #     if lemmatized_word != word:
        #         if lemmatized_word in doc_freq:
        #             doc_freq[lemmatized_word][0] += word_stop_list.count(word)
        #         else: 
        #             doc_freq[lemmatized_word] = [word_stop_list.count(word), 0]
        #         if lemmatized_word in term_freq:
        #             term_freq[lemmatized_word][0] += word_stop_list.count(word)
        #             term_freq[lemmatized_word][1] += 1
        #         else:
        #             term_freq[lemmatized_word] = [word_stop_list.count(word), 1]
        #     else: 
        #         if word in doc_freq:
        #             doc_freq[word][0] += word_stop_list.count(word)
        #         else: 
        #             doc_freq[word] = [word_stop_list.count(word), 0]
        #         if word in term_freq:
        #             term_freq[word][0] += word_stop_list.count(word)
        #             term_freq[word][1] += 1
        #         else:
        #             term_freq[word] = [word_stop_list.count(word), 1]
    print(doc_chunk_list)
    for term in term_freq:
        doc_freq[term][1] += 1
    sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
    # print('sorted_freq: \n', sorted_freq[:5])
    top_10 = sorted_freq[:10]
    print(top_10)
    # sorted_freq = sorted(term_freq.items(), key=operator.itemgetter(1), reverse=True)
    # print('term_freq: \n', sorted_freq)
        
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
#     # print("Article #" + str(counter) + ': ' + article)
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
for article in tech_articles_list[:1]:
    document_path_list = ('BBC News Summary/News Articles/tech/' + article)
    summary_path_list = ('BBC News Summary/Summaries/tech/' + article)
    counter += 1
    print("Doc Article #" + str(counter) + ': ' + article)
    doc_detail(document_path_list)
    # print("Sum Article #" + str(counter) + ': ' + article)
    # doc_detail(summary_path_list)
# print("word_freq: \n ", word_freq, "\n")

# idf_calc(counter)

# sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
# print('sorted_freq: \n', sorted_freq[:5])