# jd_skill_extraction
This repo contains a unsupervised approach to extract skills from JD.


The dataset provided contains four fields:  
* ID
* Job Profile
* Job Description 
* Category

The problem statement is:
Input JD: "Experience in Java is a must. Knowledge of Spring, Struts, Hibernate etc. Should be good with algorithms, data structures. Should have working knowledge of GIT. Should have worked in an agile environment. Communication skills should be great."  

Output Keywords: Java, Spring, Struts, Hibernate, algorithms, data structures, GIT, agile environment, communication skills.  

Given input JD, the task is to get all the skill keywords included in the document.

After checking the frequency of Job Profile in the dataset, we can figure out that very few number of job profiles are repeated significant number of time. So Job Profile may not be the best features to consider at this point.

Let's check frequency of column "Category".  

({'PR, Advertising & Marketing Jobs': 123, 'Maintenance Jobs': 121, 'Retail Jobs': 106, 'Healthcare & Nursing Jobs': 101, 'Accounting & Finance Jobs': 100, 'Energy, Oil & Gas Jobs': 99, 'IT Jobs': 99}). 

As we can see, we have some 7 odd categories with almost same number of Job Descriptions. So this column "Category" can be considered for our modeling purpose.  

One more thing, the skills are going to be noun chunks. So if we can extract noun chunks from the text, it will have all the candidates who can preferably be included in Skills.  

So let us extract noun chunks from the text.  

After extracting the noun chunks, we can note that only these chunks or let's say only these nouns matter to us (Just to add, understanding English Sentence Structure will only add to complexity).  

So we finally have our chunks. We need a set of Skills which are a subset of our chunk set. So, we need some proper mechanism to filter out unwanted nouns. One ways to do that will be, to treat each job description as a Document and compute TF-IDF score for each word in the document. So in this case, we need to discard, the words with Low TF-IDF score as well as High TF-IDF socre.  
* words with low TF-IDF score indicate the term is present across all the document, so it may be a stop word. [Assumption]. 

* words with high TF-IDF score indicate the term is only specific to that document. However, we have several document in our dataset, which belong to same job category. So, Job skills in same job category must be related. So, job skills will never get high TF-IDF score. [Assumption]  

Interestingly, we have total 749 documents and documents have total 5946 unique nouns. So, each document on average has 7 unique words. This seems highly unlikely as the number of nouns in each document are expected to be much more than this. So, we can expect a good amount of overlap of words between documents.  

