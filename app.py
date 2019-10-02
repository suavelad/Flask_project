import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
# from flask_paginate import Pagination, get_page_parameter


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "tweet.db"))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

# csv_path = '/home/s/Documents/Projects/Challenge1/python_tip_tweets.csv'
# df=pd.read_csv(csv_path)
# df.rename(columns={"Timestamp":"datetime","Python Tip:":"tips","Your name or Twitter id:":"handle"},inplace=True)
# df.dropna(subset=['datetime','handle'],axis=0, inplace=True)


# Create our database model
class Tweets(db.Model):
    # __tablename__ = "users"
    Id = db.Column(db.Integer, primary_key=True)
    who_posted = db.Column(db.String(120))
    python_tip = db.Column(db.String(200))
    # link = db.Column(db.String(200), unique=True)
    date_time = db.Column(db.String(120),unique=True)

    # def __init__(self, who_posted, python_tip, link, date_time):
    def __init__(self, who_posted, python_tip, date_time):

        self.who_posted = who_posted
        self.python_tip = python_tip
        # self.link = link
        self.date_time = date_time

    def __repr__(self):
        return '<Tweet by %r posted>' % self.who_posted


# Set "homepage" to index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    csv_path = '/home/s/Documents/Projects/Python Projects/Challenge1/python_tip_tweets.csv'
    df=pd.read_csv(csv_path)
    df.rename(columns={"Timestamp":"datetime","Python Tip:":"tips","Your name or Twitter id:":"handle"},inplace=True)
    df.dropna(subset=['datetime','handle'],axis=0, inplace=True)
    # page = request.args.get(get_page_parameter(), type=int, default=1)

    # if (request.form):
    #     tweeting = Tweets(
    #         who_posted=request.form.get('who_posted'),
    #         python_tip=request.form.get('python_tips'),
    #         link=request.form.get('link'), 
    #         date_time=request.form.get('date_time')
    #     )
    for tweet in df.itertuples():
        try:

            tweeting = Tweets(
                    who_posted=tweet.handle,
                    python_tip=tweet.tips,
                    # link=tweet.link, 
                    date_time=tweet.datetime
                )
            db.session.add(tweeting)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session().rollback()

    tweets = Tweets.query.all()
    # pagination = Pagination(page=page, total=tweets.count(1),  record_name='tweets')

    return render_template('index.html', tweets=tweets)


@app.route('/delete', methods=['POST'])
def delete():
    date_time = request.form.get('date_time')
    tweet = Tweets.query.filter_by(date_time=date_time).first()
    db.session.delete(tweet)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8000)