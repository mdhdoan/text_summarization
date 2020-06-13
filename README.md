# text_summarization
Extractive summary of BBC articles | News Articles is included

# Abstracts:
Given the fact that there are too many news articles, how can one summarize them automatically? With this, the paper now focuses on performing TFIDF on each noun phrases of each article to then rank the sentences that has them and combined them into summaries.

# Introduction:
According to the Worldometer, an online tool that counts how many posts are made in **WordPress.com**, there are easily millions of posts made everyday. This creates a problem that no one has time to read through all of them. One of the clear example of this problem is the news. They can make as many articles as they want, but if there are too much, no one can read through all of them. That's why news companies started to create a small summary with their headlines. The summary, while a little bit bias to hook the readers, also serves the purpose of summarizing the idea of the article to save time for the reader.  
The dataset used in this problem will be from [BBC News][https://github.com/mdhdoan/text_summarization/tree/master/BBC%20News%20Summary]

# Problem:
The presented problem now brings in a question:  
**How can one summarize an article automatically?**  
And after creating a summary, how can one evaluate if the summary is correct or not?  
In this problem, the dataset of BBC news articles will be used. Along with it, there are a baseline summary given for each article. Those will be used to compare to the generated summaries.  
# Solution:
In this problem, an **extract-based method** will be deployed.  
To start with, there is a need to filter all the stop words, since they are not vital to the calculation, and will only serve to skew the data. After that, there will also be a need to lemmatize and stemming all the words, so each word is reverted back to its root form. This will aid in the calculation of term frequency. The most important step, is to calculate the Term Frequency over Inverse Document Frequency (**TFIDF**). This will give each word a seperate weight, and consequently, each sentence will also have their own. The sentences can then be ranked, and the summary can have a limit to how many sentences/how important each sentences need to create a comprehensible summary.  
In order to achieve this, a method called "chunking" can be deployed. It will find the words that is going to be used, and collect them into a set of words. These can be refered to as **"Noun Phrase" - NP**. These NP can be organized into sets, which will allow the search to find duplicates throughout all the documents. Last but not least, the NP's length - the length of the whole Noun Phrase - must also be taken into consideration. Based on the assumption of treating the NP as a set of words, the maximum amount of subset from a set is 2^n, where n is the length of the set. Therefore, each NP will be boosted to with their respective boost.
Another factor to consider is the length of the summaries. A summary should not take too long to read, since readers either skim them and the headlines to rudimentarily guess what the article is about and whether it intrigues them or not. Therefore, the length of the summaries will be limited to about 5 sentences. This will allow the readers to read through them quickly, but not too long, that they would ignore them. 
# Analyzing application:

# Drawbacks:
In the process above, there are a few drawbacks. First of all: The summaries provided by the dataset [Summaries][https://github.com/mdhdoan/text_summarization/tree/master/BBC%20News%20Summary/Summaries] did not published their way of attaining the solution. This led to a situation where it is experimental work to replicate their summaries. Therefore, there are no way of comparing the summaries, without being subjective about them. 
Another drawback is the usage of TFIDF for each term. In the cases of multiple NP, how does one properly boost each one to show their importance? The longer the NP is, usually the more important they are, but what if there is another way?
# Conclusion:
In the end, these are the summaries achieved via performing TFIDF.
# Source:
* Dataset's [source](https://www.kaggle.com/pariza/bbc-news-summary/data)  
* Worldometers' post [counter](https://www.worldometers.info/blogs/)
