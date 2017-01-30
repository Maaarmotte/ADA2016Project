# ADA2016Project

## Abstract
The goal of our project is to generate some happy maps for cities in Switzerland by following the work done by the GoodCityLife team. We are interested to find out, which locations in Switzerland are the happiest by analysing the sentiments associated with different location shared on social networks.  

In our project we looked at the whole Switzerland and found out, which cities can be associated with more or less positive sentiments. 

## Project description
By making use of the crowdsourced information, we could construct a map with cities fulfilling peoples desire for an emotionally satisfying experience. We assume that positive tweets related to a city correspond with the positive general opinions about those cities, thus the more positive tweets the more likely the city or location is perceived to induce positive feelings.

Our analysis is mostly based on the 10 months Twitter data gathered from April to October 2016.
We analysed people's sentiment in regard to diffrent cities, which required Natural Language Processing (NLP). To classify locations either as likeable or not likeable, we used some machine learning tools like the Bayes classification in order to match tweets without sentiments with tweets, which contained the provided sentiment data.

## Extracting data
We were provided with the database on a cluster for Twitter, Instagram and News data. 


## Processing
We implemented Bayes classification methods to classify tweets without sentiments given the tweets with provided sentiments as the training data. 

The initial data gathered from the Twitter database conatined lots of meaningless information and some non-latin characters. Therefore we first needed to clean the data about locations and leave only the locations for, which we could get the coordinates with GeoPy geogoding package for Python.


## Visualizations
First we used the Folium package to create some simple maps with cities mapped with balloons colored either red or green depending on whether the majority of sentiments were negative or positive.

To add interaction we made use of the Leaflet library. We were able to project the sentiments by language and added a timeslider to show changes over the 10 months.


## Feasibility and Risks
The major challenge was to estimate the amount and kind of work, which would be required to fulfil our expected outcome. For example, using NLP to find either positive or negative experiences connected with certain locations could become very complicated if pushed too far. Moreover, none of us have any experience with NLP, so we expected it to be challenging.

A great part of our project was to develop an interactive map, which would be visually appealing and contain the data about the cities and sentiments grouped by months and languages. 

## Future developments
Our project scope could be increased to take into account a longer time period and data from other sources such as Flickr, Instagram etc. 


## Deliverables

At the end of the project, we expect to deliver the following:
- An interactive happy map for cities and locations in Switzerland
- Comparison and description of the processing and methods used

## Timeplan
#### Checkpoint (Mid December)
- A visual representation of gathered data about happier routes and locations. 

#### Mini-Symposium (End of January)
- The final results, including everything in the _Deliverables_ section. During the presentation, we will explain how we found the results and make sense of them.
