# text_summarization
Extractive summary of BBC articles | News Articles is included

# Abstracts:

# Introduction:
According to the Worldometer, an online tool that counts how many posts are made in **WordPress.com**, there are easily millions of posts made everyday. This creates a problem that no one has time to read through all of them. One of the clear example of this problem is the news. They can make as many articles as they want, but if there are too much, no one can read through all of them. That's why news companies started to create a small summary with their headlines. The summary, while a little bit bias to hook the readers, also serves the purpose of summarizing the idea of the article to save time for the reader. 

# Problem:
The presented problem now brings in a question:  
**How can one summarize an article automatically?**  
And after creating a summary, how can one evaluate if the summary is correct or not?  
In this problem, the dataset of BBC news articles will be used. Along with it, there are a baseline summary given for each article. Those will be used to compare to the generated summaries.  
# Solution:
In this problem, an **extract-based method** will be deployed.  
To start with, there is a need to filter all the stop words, since they are not vital to the calculation, and will only serve to skew the data. After that, there will also be a need to lemmatize and stemming all the words, so each word is reverted back to its root form. This will aid in the calculation of term frequency. The most important step, is to calculate the term frequency over the document frequency (**TFIDF**). This will give each word a seperate weight, and consequently, each sentence will also have their own. The sentences can then be ranked, and the summary can have a limit to how many sentences/how important each sentences need to create a comprehensible summary.

# Analyzing application:
# Drawbacks:
# Conclusion:
# Source:
* Dataset's [source](https://www.kaggle.com/pariza/bbc-news-summary/data)  
* Worldometers' post [counter](https://www.worldometers.info/blogs/)