import nltk, os, operator
from nltk.tag import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
wnl = WordNetLemmatizer()
word_freq = {}

def doc_detail(document_path_list):
    for article in document_path_list:
        document = open(article, 'r')
        doc_freq = {}
        # print(article)
        title = document.readline()
        title_token_list = nltk.word_tokenize(title)
        # print(title_token_list)
        title_lemma_list = []
        title_tag_list = pos_tag(title_token_list)
        # print(title_tag_list)
        # syn_set = set()
        for word, tag in title_tag_list:
            if tag.startswith('JJ'):
                lemmatized_output = wnl.lemmatize(word, 'a')
                title_lemma_list.append(lemmatized_output)
                # print(tag + ': ', lemmatized_output)
            elif tag.startswith('VB'):
                lemmatized_output = wnl.lemmatize(word, 'v')
                title_lemma_list.append(lemmatized_output)
                # print(tag + ': ', lemmatized_output)
                # for syn in wordnet.synsets('seek'):
                #     for lemma in syn.lemmas():
                #         syn_set.add(lemma.name())
            elif tag.startswith('NN'):
                lemmatized_output = wnl.lemmatize(word, 'n')
                title_lemma_list.append(lemmatized_output)
                # print(tag + ': ', lemmatized_output)
            else:
                lemmatized_output = wnl.lemmatize(word)
                title_lemma_list.append(lemmatized_output)
                # print(tag + ': ', lemmatized_output)

        text = document.readlines()
        sentence_list = []
        for line in text:
            sentence_list.extend(nltk.sent_tokenize(line))
        # print(sentence_list)
        all_stopwords = stopwords.words('english')
        # print(all_stopwords)
        for sentence in sentence_list:
            # print(sentence)
            word_list = nltk.word_tokenize(sentence)
            word_stop_list = [word for word in word_list if not word in all_stopwords]
            for word in word_stop_list:
                if word.isalpha():
                    lemmatized_word = wnl.lemmatize(word)
                    if lemmatized_word != word:
                        # print(word_stop_list)
                        if lemmatized_word in word_freq:
                            word_freq[lemmatized_word] += word_stop_list.count(word)
                        else: 
                            word_freq[lemmatized_word] = word_stop_list.count(word)
                        if lemmatized_word in doc_freq:
                            doc_freq[lemmatized_word] += word_stop_list.count(word)
                        else:
                            doc_freq[lemmatized_word] = word_stop_list.count(word)
                    else: 
                        if word in word_freq:
                            word_freq[word] += word_stop_list.count(word)
                        else: 
                            word_freq[word] = word_stop_list.count(word)
                        if word in doc_freq:
                            doc_freq[word] += word_stop_list.count(word)
                        else:
                            doc_freq[word] = word_stop_list.count(word)

        # for word1 in title_lemma_list:
        #     frequency = 0
        #     for sentence in sentence_list:
        #         # print(sentence)
        #         word_list = nltk.word_tokenize(sentence)
        #         word_stop_list = [word for word in word_list if not word in all_stopwords]
        #         for word2, tag in pos_tag(word_stop_list):
        #             if word2 == word1:
        #                 frequency += 1
            # print(word1 + ' frequency: ', frequency)
        # sorted_freq = sorted(doc_freq.items(), key=operator.itemgetter(1), reverse=True)
        # print(sorted_freq)

business_articles_list = os.listdir('BBC News Summary/News Articles/business/')
entertainment_articles_list = os.listdir('BBC News Summary/News Articles/entertainment/')
politics_articles_list = os.listdir('BBC News Summary/News Articles/politics/')
sport_articles_list = os.listdir('BBC News Summary/News Articles/sport/')
tech_articles_list = os.listdir('BBC News Summary/News Articles/tech/')
document_path_list = []

# for article in business_articles_list:
#     document_path_list.append('BBC News Summary/News Articles/business/' + article)
#     doc_detail(document_path_list)
# document_path_list = []
# for article in entertainment_articles_list:
#     document_path_list.append('BBC News Summary/News Articles/entertainment/' + article)
#     doc_detail(document_path_list)
# document_path_list = []
# for article in politics_articles_list:
#     document_path_list.append('BBC News Summary/News Articles/politics/' + article)
#     doc_detail(document_path_list)
# document_path_list = []
# for article in sport_articles_list:
#     document_path_list.append('BBC News Summary/News Articles/sport/' + article)
#     doc_detail(document_path_list)
# document_path_list = []
for article in tech_articles_list:
    document_path_list.append('BBC News Summary/News Articles/tech/' + article)
    doc_detail(document_path_list)
sorted_freq = sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)
print(sorted_freq)