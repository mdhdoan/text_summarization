# text_summarization
Extractive summary of BBC articles | News Articles is included

# Abstracts:
Given the fact that there are too many written articles being produced daily, how can one summarize them automatically for their own purposes? This paper focuses on performing automatic summarization on news articles. The main method deployed in this publish will be a crude automatic extractive summarization, based on [Term Frequency over Inverse Document Frequency](https://en.wikipedia.org/wiki/Tf–idf) of each phrases. 

# Keywords:
text summarization, extractive summarization, TFIDF

# Introduction:
According to the Worldometer, an online tool that counts how many posts are made in **WordPress.com**, there are easily millions of posts made everyday. This creates a problem that no one has time to read through all of them. One of the clear example of this problem is the news. They can make as many articles as they want, but if there are too much, no one can read through all of them. That's why news companies started to create a small summary with their headlines. The summary, while a little bit bias to hook the readers, also serves the purpose of summarizing the idea of the article to save time for the reader.  
The dataset used in this problem will be from [BBC News](https://github.com/mdhdoan/text_summarization/tree/master/BBC%20News%20Summary)

# Problem:
The presented problem now brings in a question:  
**How can one summarize an article automatically?**  
And after creating a summary, how can one evaluate if the summary is correct or not?  
In this problem, the dataset of BBC news articles will be used. Along with it, there are a summary given for each article. The summaries can be used as a goal to reach, or to surpass in terms of summarizing the news articles. Those will be used to compare to the generated summaries.  
# Solution:
In this problem, an **extractive automatic summarization** will be deployed. The method would simply be ranking each sentences in a news article by their weight of each phrase. 
### Extractive automatic summarization:
A summarization that produce a result of phrases/sentences presented in the article. This approach contains an advantage of not needed to understand the topic of the articles, while also have a disadvantage in the dependency of the article's words.  
The method can be presented in the following steps:  
## Step 1: Looking for Noun Phrase - NP - in each sentences.  
To start with, there is a need to filter all the stop words, since they are not vital to the calculation, and will only serve to skew the data. After that, there will also be a need to lemmatize and stemming all the words, so each word is reverted back to its root form. In addition to that, a method called "chunking" will be deployed. It will find the words that is going to be used, and collect them into a set of words. These can be refered to as **"Noun Phrase" - NP**. These NP can be organized into sets, which will allow the search to find duplicates throughout all the documents.  
## Step 2: Calculating TFIDF of NP: 
After categorizing the noun phrases, one can trace over the articles to see how many times a phrase is repeated. This will aid in the calculation of term frequency. The most important step, is to calculate the [Term Frequency over Inverse Document Frequency](https://en.wikipedia.org/wiki/Tf–idf) (**TFIDF**). This will give each word a seperate weight, and consequently, each sentence will also have their own.  
## Step 3: Create summaries:
The sentences can then be ranked, and the summary can have a limit to how many sentences/how important each sentences need to create a comprehensible summary.  
 Last but not least, the NP's length - the length of the whole Noun Phrase - must also be taken into consideration. Based on the assumption of treating the NP as a set of words, the maximum amount of subset from a set is 2^n, where n is the length of the set. Therefore, each NP will be boosted to with their respective boost.
Another factor to consider is the length of the summaries. A summary should not take too long to read, since readers either skim them and the headlines to rudimentarily guess what the article is about and whether it intrigues them or not. Therefore, the length of the summaries will be limited to about 5 sentences. This will allow the readers to read through them quickly, but not too long, that they would ignore them. 
# Analyzing application:
## NP analyze:
Firstly, the article is "chunked" into NP that is set. In this case, NP are Nouns who are preceeded only by adjective, verbs, or other nouns. "Big market" would be acceptable, but not "The market", since "The" is not an adjective/verb/noun.  
![NP](https://github.com/mdhdoan/text_summarization/blob/master/Terminal%20pictures/Screen%20Shot%202020-06-13%20at%2010.34.32%20AM.png)  
In this case, since only one document is being process for the sake of the example, the tfidf is the one mentioned above, whereas the tf is the term frequency, and the idf is the inverse document frequency. The detail included are stating which document they belong (each category has their own set of NP, so no worries about duplications of documents id for now), then how many times the term appeared in the document, followed by how many times the NP appears in a sentence, and which sentence it is.  

For longer NP, they can be separated by "\*\*"  
![Longer NP](https://github.com/mdhdoan/text_summarization/blob/master/Terminal%20pictures/Screen%20Shot%202020-06-13%20at%2010.34.49%20AM.png)  
## Sentence Pairing with NP:
After being chunked and calculated their own TFIDF, then each documents are then re-examined to pair up the sentences with their NPs.  
![pairing](https://github.com/mdhdoan/text_summarization/blob/master/Terminal%20pictures/Screen%20Shot%202020-06-13%20at%2010.35.17%20AM.png)  
At this stage, the number next to each NP is their respective TFIDF, before being boosted.  
## Result sentences ranked and written into files:
Lastly, the summaries are made of 5 sentences, so the job is to rank the sentences in each documents to produce the top 5 sentences with respect to their sentences's TFIDF.  
![Result rank](https://github.com/mdhdoan/text_summarization/blob/master/Terminal%20pictures/Screen%20Shot%202020-06-13%20at%2010.35.30%20AM.png) 
All results are then put into ["My Summaries"](https://github.com/mdhdoan/text_summarization/tree/master/My%20Summaries) 

# Drawbacks:
In the process above, there are a few drawbacks. First of all, the summaries provided by the dataset [Summaries](https://github.com/mdhdoan/text_summarization/tree/master/BBC%20News%20Summary/Summaries) did not published their way of attaining the solution. This led to a situation where it is experimental work to replicate their summaries. Therefore, there are no way of comparing the summaries, without being subjective about them. 
Another drawback is the usage of TFIDF for each term. In the cases of multiple NP, how does one properly boost each one to show their importance? The longer the NP is, usually the more important they are, but what if there is another way?
Lastly, News are subjective, in their own ways, so perhaps summarizing with and "abstractive method" would have been more useful? Since only the idea of the reporter should be kept, and the wordings can also be biased.
# Conclusion:
In the end, these are the summaries achieved via performing TFIDF. There are many ways of summarizing news articles. Since this is not a precise science, each of the results from these ways can be subjectively ranked. The important thing to draw from this is that summarizing with TFIDF can only do so much, and while the world is searching for, perhaps, the best way to summarize news articles, TFIDF remains as one of the most popular way.
# Source:
* Dataset's [source](https://www.kaggle.com/pariza/bbc-news-summary/data)  
* TFIDF [source] (https://en.wikipedia.org/wiki/Tf–idf)
* Worldometers' post [counter](https://www.worldometers.info/blogs/)
