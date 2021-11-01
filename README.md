# Vandymen

## Brief
This web project was developed for the Vandymen Wiffle Ball League at Vanderbilt University. 
The website was created using Django and holds stats, standings, prediction capabilities, and more, for the league and its players.
It is currently hosted [here](https://vandymen.herokuapp.com/).

## Full Description
The website consists of the following major pages.
* `Stats` - Contains statistic leaders for common batting categories like hits, home runs, and rbi's
* `Standings` - Shows the current team standings for each division of the league.
* `Teams` - A list of all teams in the league. Clicking on ay team will show detailed view of the record and recent performances.
* `Players` - A list of all players in the league. Clicking on any player will show a detailed view of them and their stats.
* `Mock Draft` - Using linear regression with sklearn, a model takes into consideration a players tendency for hits, home runs, and walks and estimates the
number of runs they will generate in a game. The computer then selects players in order of this predicted output in a "draft".
* `Matchup Predictor` - A form that takes two teams and predicts the result of a series between them. Uses a simulation of games between the two
using normal distributions created from information about that team and their opponent such as their average runs scored or the opponents average. runs allowed.
* `FAQ` - Answers frequently asked questions.

In addition, the website allows, in many areas, for teams or players to be clicked on for more detail.
Major django models used in this project are defined in models.py in the statsApp folder.
PlayerList, TeamList, PlayerDetail, and TeamDetail are all views that extend `Django generic views`. 
The site itself is hosted on Heroku using the `django-heroku` library and the heroku CLI.


## Requirements
* asgiref==3.2.10
* Bottleneck==1.3.2
* certifi==2021.10.8
* dj-database-url==0.5.0
* Django==3.1
* django-heroku==0.3.1
* gunicorn==20.1.0
* joblib==1.1.0
* numexpr==2.7.3
* numpy==1.21.3
* pandas==1.3.3
* plotly==5.3.1
* psycopg2==2.9.1
* python-dateutil==2.8.2
* pytz==2021.3
* scikit-learn==1.0.1
* scipy==1.7.1
* six==1.16.0
* sklearn==0.0
* sqlparse==0.4.2
* tenacity==8.0.1
* threadpoolctl==3.0.0
* typing-extensions==3.10.0.2
* whitenoise==5.3.0

## Acknowledgements
Thank you to Connor Campbell and Chris Wiley for creating the Vandymen league and keeping the game stats! <br>
This website is not offiliated with Vanderbilt University.


