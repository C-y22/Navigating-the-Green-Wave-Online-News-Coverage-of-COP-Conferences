# Navigating-the-Green-Wave-Online-News-Coverage-of-COP-Conferences

The code and data in this repository is a reproducible research workflow for "Navigating the Green Wave: Computational Insights into of Environmental Discourse in Online News Coverage of COP Conferences!" of Master Thesis at the University of Chicago.

## How to use it

The code is written in Python 3.8.16 and all of its dependencies can be installed by running the following in the terminal (with the `requirements.txt` file included in this repository):

```
pip install -r requirements.txt
```
Note: time, datetime, warnings, and hashlib are python build-in module, so they are not included in the requirements.txt

The scrapped datasets being analyzed are too big to upload to GitHub, so here is the link: https://drive.google.com/file/d/1ZxrRfESmmTWii27er-DJmzgsxNlG59ru/view?usp=sharing


Then, you can import the `fox`, `sun` and `cnn` module located in this repository to reproduce the web-scrapping process in the (hypothetical) publication that this code supplements (in a Jupyter Notebook, like README.ipynb in this repository, or in any other Python script): 


```python
import fox
import cnn
import sun
```

The `FrequencyAnova2.ipynb` contains the codes for the ANOVA analysis of the number of news for different time intervals of the data. 

The `Sentiment_Analysis5.ipynb` contains the codes for the sentiment analysis of the data. 

The `TopicModeling6.ipynb` contains the codes for the LDA topic modeling of the data. 

The `monthly2020-2023.zip` contains the results of topic modeling. 

The `frequency2.5.ipynb` contains the codes for the frequency analysis the data. 


## Initial Findings

"carbon emission" is one of the most relevant keywords related to the Paris Agreement. The frequency of it based on years matches with the "issue attention cycle" well, because the curve starts to go up before 2015 (the year of the Paris Agreement), reaches a peak at 2015, and then goes down, which matches with the five stages in the theory (re-problems stage, alarmed discovery and euphoria stage, realizing the cost of significant progress stage, gradual decline of public interest stage, post-problem stage) . 

https://github.com/macs30200-s23/replication-materials-chunyang/blob/main/carbonemission.jpeg
![carbon emission frequency from 2011-2022](https://github.com/macs30200-s23/replication-materials-chunyang/blob/main/carbonemission.jpeg)

## How to cite this

To cite this reposotiry in APA, please use:

Zhang, Chunyang. (2024, April 15). replication-materials-chunyang. GitHub. [https://github.com/macs30200-s23/replication-materials-chunyang.git](https://github.com/C-y22/Navigating-the-Green-Wave-Online-News-Coverage-of-COP-Conferences.git)

For in-text citation:

(Zhang, 2024)

I will use this citation in the following situations in the final paper: data collection methods, data processing procedures, data visualization, interpretation of results and discussion.
