# News App
A web application is built using Python framework (Flask) and BART LLM. The app displays information about news articles from popular sources, provides Machine Learning functionalities like summarization and chatbot

## Functions
The user can perform the following functions:

- See latest news on the homepage of the application
- Select a news and chat with a chatbot about it and its related topics.
- Select a news and read it in 15s.
- Click on an article and read the full article.

## Technologies Used
- python 3.11

## Project Setup Instructions (Using in Terminal)
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
$ python3 -m venv env
```
4. activate env
```
$ source env/bin/activate
```
5. install Dependencies
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
9. Paste the url(default: http://127.0.0.1:5000, but please check on your terminal) into the web browser and run the model!


