CS 432/532 Web Science
Spring 2016
http://phonedude.github.io/cs532-s16/

Assignment #9
Due: 11:59pm April 21 2016

Support your answer: include all relevant discussion, assumptions,
examples, etc.

1.  Choose a blog or a newsfeed (or something similar with an Atom
or RSS feed).  Every student should do a unique feed, so please
"claim" the feed on the class email list (first come, first served).
It should be on a topic or topics of which you are qualified to
provide classification training data.  Find something with at least
100 entries (or items if RSS).

Create between four and eight different categories for the entries
in the feed:

examples: 

work, class, family, news, deals

liberal, conservative, moderate, libertarian

sports, local, financial, national, international, entertainment

metal, electronic, ambient, folk, hip-hop, pop

Download and process the pages of the feed as per the week 12 
class slides.

Be sure to upload the raw data (Atom or RSS) to your github account.

2.  Manually classify the first 50 entries, and then classify (using
the fisher classifier) the remaining 50 entries. 

Create a table with the title, predicted category, actual category,
and cprob() and fisherprob() for the actual category.

3.  Assess the performance of your classifier in each of your
categories by computing precision, recall, and F-measure.  

===================================================================
========The questions below is for 3 points extra credit===========
===================================================================

4.  Redo the questions above, but with the extensions on slide 27
and pp. 136--138.

===================================================================
========The questions below is for 3 points extra credit===========
===================================================================

5.  A 1:1 split for training:test data typically not a good split;
5:1 or even 10:1 is preferable.  We also typically use something
called "10-fold cross validation" to make sure we spread the training
out and don't "overfit" on a particular sequence of tranining data.

Rerun questions 2 & 3, but manually classifying all 100 documents,
then using 90 for training and 10 for testing.  Use 10-fold cross
validation and generate the table from Q2, but this time with the
average of all 10 values.  What was the change, if any, in precision
and recall (and thus F-Measure)?