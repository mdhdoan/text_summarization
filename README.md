# Automatic Extraction-based summarization of BBC articles |

# Abstracts:
Given the fact that there are too many written articles being produced daily, how can one summarize them automatically for their purposes? This paper focuses on performing automatic summarization on news articles. The main method deployed in this publish will be a crude automatic extraction-based summarization, based on [Term Frequency over Inverse Document Frequency](https://en.wikipedia.org/wiki/Tf–idf) - (**TFIDF**) of each phrase. 

### Keywords:
text summarization, extraction-based summarization, TFIDF


# 1. Introduction:
According to the Worldometer, an online tool that counts how many posts are made in WordPress.com, there are easily millions of posts made every day. This creates a problem that no one has time to read through all of them. One of the clear examples of this problem is the news articles produced every day. They can make as many articles as they want, but if there are too many, no one can read through all of them. That's why news companies started to create a small summary with their headlines. The summary, while a little bit bias to hook the readers, also serves the purpose of summarizing the idea of the article to save time for the reader.
The dataset used in this problem will be from [BBC News](https://github.com/mdhdoan/text_summarization/tree/master/BBC%20News%20Summary)


# 2. Problem:
The presented problem now brings in a question:  
**How can one summarize an article automatically?**  
And after creating a summary, how can one evaluate if the summary is correct or not?
In this problem, the dataset of BBC news articles will be used. Along with it, there is a summary given for each article. The summaries can be used as a goal to reach or to surpass in terms of summarizing the news articles. Those will be used to compare to the generated summaries.


# 3. Extraction-based summarization:
A summarization that produces a result of phrases/sentences presented in the article. This approach contains an advantage of not needed to understand the topic of the articles, while also have a disadvantage in the dependency of the article's words.  


# 4. Solution:
In this problem, an **extraction-based automatic summarization** will be deployed. The method would simply be ranking each sentence in a news article by the weight of each phrase.  

## 4.1. Looking for Noun Phrase - in each sentences.  
Too start with, there is a need to filter all the stop words, since they are not vital to the calculation, and will only serve to skew the data. After that, there will also be a need to lemmatize and stemming all the words, so each word is reverted to its root form. In addition to that, a method called "chunking" will be deployed. It will find the words that are going to be used and collect them into a set of words. These can be referred to as **"Noun Phrase"**. These Noun phrases can be organized into sets, which will allow the search to find duplicates throughout all the documents.
Also, in the process of creating the list of phrases and its detail, the phrase must be lemma before stemming, since stemming can produce the wrong word.  

## 4.2. Calculating TFIDF of Noun Phrase: 
After categorizing the noun phrases, one can trace over the articles to see how many times a phrase is repeated. This will aid in the calculation of term frequency. The most important step is to calculate the TFIDF. This will give each word a separate weight, and consequently, each sentence will also have their own.  
During the calculation, it is easier to refer to each noun phrases as a key, and the values associated (when needed), so that each time accessing a key, all of its values can be extracted easily.  

## 4.3. Create summaries:
The sentences can then be ranked, and the summary can have a limit to how many sentences/how important each sentence needs to create a comprehensible summary.
However, there can be many ways to improve the ranking of the sentences:
* Noun Phrase's length - the length of the whole Noun Phrase - must also be taken into consideration. Based on the assumption of treating the Noun Phrase as a set of words, the maximum amount of subset from a set is 2^n, where n is the length of the set. Therefore, each Noun Phrase will be boosted with their respective boost  
* Summaries' length - A summary should not take too long to read since readers either skim them and the headlines to rudimentarily guess what the article is about and whether it intrigues them or not. Therefore, the length of the summaries will be limited to about 5 sentences. This will allow the readers to read through them quickly, but not too long, that they would ignore them. 


# 5. Analyzing application:

## 5.1. Noun Phrase analyze:
In this case, the Noun Phrase is Nouns who are preceded only by adjectives, verbs, or other nouns. "Big market" would be acceptable, but not "The market", since "The" is not an adjective/verb/noun.
In this case, the ruleset is the following: 
* A noun phrase must contain all the verbs/adjectives right before, while also grabbing as many nouns clumped together as possible
* Also Pronouns are considered as a noun phrase too  

Using the grammar rule above, when running the program, the noun phrases can be viewed with the following design:  
> ![Noun Phrase](https://github.com/mdhdoan/text_summarization/blob/master/Terminal%20pictures/Screen%20Shot%202020-06-13%20at%2010.34.32%20AM.png)  

In this case, since only one document is being processed for the sake of the example, the "tfidf" is the one mentioned above, whereas the "tf" is the term frequency, and the "idf" is the inverse document frequency. The detail included is stating which document they belong (each category has their own set of Noun Phrase, so no worries about duplications of documents id for now), then how many times the term appeared in the document, followed by how many times the Noun Phrase appears in a sentence, and which sentence it is.
For longer Noun Phrase, they can be separated by "\*\*"  
> ![Longer Noun Phrase](https://github.com/mdhdoan/text_summarization/blob/master/Terminal%20pictures/Screen%20Shot%202020-06-13%20at%2010.34.49%20AM.png)  

## 5.2. Sentence Pairing with Noun Phrase: 
After being chunked and calculated their TFIDF, then each document is then re-examined to pair up the sentences with their Noun Phrases. The Noun Phrase can be used to further lemmatized, which would enable similar phrases, such as "good people", and "nice people" to both be understood as talking about people.
The phrases, when being revisited to count their frequencies in a document, can then be pair with each sentence, hence creating a key-value pairing system. Each sentence can be the key, and the phrases can be the values, which will store their TFIDF for calculation.  
The principle behind this is like the illustration below:  
Original text:  
> ![Original text](https://github.com/mdhdoan/text_summarization/blob/master/Extra/Article.png)  

Then being paired up with extracted noun phrases:  
> ![paired](https://github.com/mdhdoan/text_summarization/blob/master/Extra/Sentence%20pairing.png)

In the middle of the program, the TFIDF of each noun phrases will be included, after being boosted in respect to the length of each noun phrase.  
> ![NP-pairing](https://github.com/mdhdoan/text_summarization/blob/master/Extra/Screen%20Shot%202020-06-18%20at%208.32.01%20PM.png)


## 5.3. Result sentences ranked and written into files:
Lastly, the summaries are made of 5 sentences, as agreed upon above, so the job is to rank the sentences in each document to produce the top 5 sentences concerning their sentences' TFIDF.
> ![ranked](https://github.com/mdhdoan/text_summarization/blob/master/Extra/ranking.png)  

While in the program, each sentence will have the following format, where each sentence has 2 numerical values, where the second number is the important value: sentence's weight.
The result can be a little bit difficult to imagine, so below are 2 summaries, one provided by BBC and the other is produced by the method in step 4.  
Given summary | Produced summary:  
> ![G|P](https://github.com/mdhdoan/text_summarization/blob/master/Extra/Screen%20Shot%202020-06-18%20at%208.28.34%20PM.png) 

While the given summary is longer, most - in red color above - (and the entirety in some cases) of the produced summaries are included in the given summary. Since summaries are supposed to be short and carry the important ideas only, it is safe to say that the produced result is acceptable.    
All results are then put into [My Summaries](https://github.com/mdhdoan/text_summarization/tree/master/My%20Summaries), for future usage and collection.


# 6. Drawbacks:
* In the process above, there are a few drawbacks. First of all, the summaries provided by the dataset [Summaries](https://github.com/mdhdoan/text_summarization/tree/master/BBC%20News%20Summary/Summaries) did not publish their way of attaining the solution. This led to a situation where it is experimental work to replicate their summaries. Therefore, there is no way of comparing the summaries, without being subjective about them.   
* Another drawback is the usage of TFIDF for each term. In the cases of multiple Noun Phrase, how does one properly boost each one to show their importance? The longer the Noun Phrase is, usually the more important they are, but what if there is another way?
* Also, News articles are subjective, in their ways, so perhaps summarizing with and "abstractive method" would have been more useful? Since only the idea of the reporter should be kept, and the wordings can also be biased.  
* Lastly, the evaluation of the summaries. How can one rank the summaries from best to worst? Currently, there is no ideal summary of a document. Many methods proposed, such as [ROUGE](https://en.wikipedia.org/wiki/ROUGE_(metric)), and others used in evaluation contests ([SUMMAC](https://www-nlpir.nist.gov/related_projects/tipster_summac/), [DUC](https://duc.nist.gov), [TAC](https://tac.nist.gov), ...), all required human intervention. However, not all documents have an optimal summary available, or a human who can judge all the time.


# 7. Conclusion:
The number of articles is increasing in a huge magnitude every day. Without enough time in a day, no one can comprehend all the information. Therefore, a need for automatic summarization is developed. This paper, while not being the most innovative nor the best implementation of a method, solved the need for summaries via performing an extraction-based method, with the help of TFIDF. There are many ways of summarizing news articles. There are many scientific ways to evaluate the summaries, but in the end, each of the results can be ranked subjectively. Although not reaching the optimal solution, this paper still provides a good insight into a method and its implementation.  

# 8. Source:
* Dataset's [source](https://www.kaggle.com/pariza/bbc-news-summary/data)  
* TFIDF [source] (https://en.wikipedia.org/wiki/Tf–idf)
* Worldometers' post [counter](https://www.worldometers.info/blogs/)
