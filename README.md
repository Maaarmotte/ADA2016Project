# ADA2016Project
*Please note this is only a short proposal, as we didn't get the confirmation from M. Catasta yet. This might be modified in the future, after the deadline.*

## Abstract
The goal of our project is to analyze data from Reddit, more precisely from the /r/Switzerland subreddit. Using Natural Language Processing (NLP), the main discussion topics can be extracted to see the current interests of people. By analyzing the names of the posts, their content, and the descriptions from the side-bars of the subreddits, a description of how /r/Switzerland is linked to other subreddits can be made. The profiles of the people posting give information about recent posted messages. This allows us to see on which other subreddits people posting in /r/Switzerland are active.

## Data description
The data that are going to be used are extracted from Reddit using the official API. We didn't collect them ourselves, they are given with the project. We couldn't access them yet, but we suppose they contain at least the following:
- Topic of discussion (title)
- Original message
- Answers and comments from other people
- Dates of all messages
- Usernames of the participants

## Feasability and Risks
The major problem is to estimate how much work will be required. For example, using NLP to find the main discussion topics can be very complicated if pushed too far. We will have to analyze how well we are doing and modify our expectations over time. Moreover, none of us have any experience with NLP, so we expected it to be challenging.

## Deliverables
At the end of the project, we expect to deliver the following:
- A graph representing the links between /r/Switzerland and other subreddits.
- A list of most discussed topics
- A graph showing on which subreddits people from /r/Switzerland are also active
As well as the interpretation of these results.

## Timeplan
#### Checkpoint (Mid December)
- The graph of the related subreddits as well as the current work on other objectives.

#### Mini-Symposium (End of January)
- The final results, including everything in the _Deliverables_ section. During the presentation, we will explain how we find these results and make sense of them.
