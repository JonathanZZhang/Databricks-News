import os,threading,time,schedule
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from news.db import get_db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    
    @app.route('/')
    def index():
        db = get_db()
        articles = db.execute(
            'SELECT id, title, body, created' 
            ' FROM article ORDER BY created DESC'
            ).fetchmany(20)
        return render_template('index.html', articles = articles)
    
    def get_article(id, check_author = True):
        article= get_db().execute(
            'SELECT id, title, body, summary'
            ' FROM article'
            ' WHERE id = ?',
            (id,)
        ).fetchone()

        if article is None:
            abort(404, f"article id {id} doesn't exist.")
    
        return article

    @app.route('/<int:id>/show')
    def show(id):
        article = get_article(id)
        return render_template('show.html', article = article)

    @app.route('/<int:id>/summarize')
    def summarize(id):
        article = get_article(id)
        if article['summary']:
            return render_template('summary.html', article = article)
        else:
            return 'Yet to be Summarized'
    
    from . import db
    db.init_app(app)

    from .scraper import get_articles
    @app.cli.command("scrape")
    def scrape_news():
        with app.app_context():
            get_articles()
    
    # schedule.every().day.at('20:15').do(scrape_news)
    
    # def scheduler_loop():
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)

    # # Start the scheduling loop in a separate thread
    # scheduler_thread = threading.Thread(target=scheduler_loop)
    # scheduler_thread.start()
    
    return app