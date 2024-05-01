# Basketball Draft Helper 
#### Video Demo:  <https://www.youtube.com/watch?v=iZXiIPC7who>
#### Description:

* What does it do?
  
Tells users how good it expects players in college to be and where it ranks them in that draft class.

* How does it do it?
1. Scores players performance in the NBA.
2. Correlates that data with their statistics playing college basketball.
3. Crunches these numbers using a machine learning algorithm to find the statistics it deems to be the most important in each position.
4. Applies the algorithm on the college players to predict how good they are.

* Why just college and not international?
  
The reason I did this was because the rules are different in other leagues and the level is different in each of these leagues so it would skew my predictions.


* Why did i choose this problem:
  
When i first started watching american sports i was always surprised by the emphasis of scouting done by 'analysts' everytime you search for mock draft in both football
and basketball it returns people's various opinions on who should be drafted where. Here in the UK there has already been a big change on how scouting is done in football
(soccer) in the last 10 years while i feel that american sports are yet to experience this shift. 

* Problems:
I created an algorithm for each position that found the correlation between players rating and there individual college statistics and then tried various combinations of
statistics to prevent overfitting. Unfortunately, even though using multiple linear regression worked reasonably well, i still feel that this could be far better executed
using machine learning. The problem is that not all great players had great seasons in college and there are some cases where they were good in college but not that good
in the nba. Because of this some of the correlations were a lot weaker/stronger than they should be in that position and some even had a negative/positive correlation 
when they should have had the opposite correlation for example one column i created was season, this column represented which year in the college they are in: In theory
this should show that players who do better in their freshman year in college should do better in the nba, however for some algorithms it had the opposite correlation meaning i couldnt use that statistic as it would incorrectly impact the scores. The website part itself is run using flask i contemplated 
creating a proper website for it but decided against it for this project so far.

The links for my data are as follows:
https://projects.fivethirtyeight.com/nba-player-ratings/ for the data i used to create ratings
https://barttorvik.com/playerstat.php?year=2022 for where i got the college statistics

Data Deals with all the backend processes so the data and website the front end

Data:

IGNORE: yr_data_split, algorithm

algorithm-pos = Creates the algorithm for each position and performs the multiple linear regression on all players
Data = Generates ratings for players and cleans the databases 
dataset_id_name = Gives each player in college dataset a unique id
Outliers_college = Gets rid off outliers in the college database
pos_data_split_train = Splits the database for each position finds the correlation and removes stats that overfit/skew it
pos_data_split_all = Does the same as above but applies it to all the players not just those in that position
scores_with_predictions = Adds the ratings generated in Data to final dataset

Website:

app = Main processes for the website
college_df_with_scores = Final dataset used
df_to_sql = Converts the dataset to a database
helpers = Contains 2 functions used in app for website
players = Database with tables for players, users and favourites
testing = Ignore i just used as a file where i would try and solve errors i didnt understand

flask_session = Ignore

static = Contains styles sheet

templates:
apology = Page for when an error occurs
change_passowrd = Page for changing users password
draft = Pages for years 2010-2022 and where the algorithm thought they should have been drafted
dyears = Page that allows you to click on the years before redirecting you to draft for that year
index = Homepage with users favourites
layout = Layout for all pages
login = Page to login 
profile = Page for each individual player in dataset
rankings = Page for rankings of players in each position for each year
ryears = Page with each year that redirects you to ranking for tha year
search = Page that allows you to search for players
searched = Page with list of results of the search


Any questions please ask.





