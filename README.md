# News App
A web application is built using Python framework (Flask) and BART LLM. The app displays information about news articles from popular sources, provides Machine Learning functionalities like summarization and chatbot

## Functions
The user can perform the following functions:

- See latest news on the homepage of the application
- Select a news and chat with a chatbot about it and its related topics.
- Select a news and read it in 15s.
- Click on an article and read the full article.

## Technologies Used
- python 3.8.8

## Project Setup Instructions
1. Git clone the repository 
```
$ git clone https://github.com/JonathanZZhang/Databricks-News.git
```
2. cd into Databricks-News
```
$ cd Databricks-News
```
3. create a virtual environment
```
$ python -m venv venv
```
4. activate venv
```
$ source venv/scripts/activate
```
5. nstall Dependancies
```
$ pip install -r requirements.txt
```
6. Initialize database
```
$ flask --app news init-db
```
7. Scrape news
```
$ flask --app news scrape
```
8. Run Application
```
$ flask --app news run
```


