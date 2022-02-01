# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
from jumbodb import Jumbo
import random
import json
import requests
from pprint import pprint

# initializes flask app:
app = Flask(__name__, template_folder='templates')

#########################
# some global variables #
#########################

# quotes = (
#     '“We May Encounter Many Defeats But We Must Not Be Defeated.” – Maya Angelou',
#     '“The Way Get Started Is To Quit Talking And Begin Doing.” – Walt Disney',
#     '“Security Is Mostly A Superstition. Life Is Either A Daring Adventure Or Nothing.” – Life Quote By Helen Keller',
#     '“The Pessimist Sees Difficulty In Every Opportunity. The Optimist Sees Opportunity In Every Difficulty.” – Winston Churchill',
#     '“Don’t Let Yesterday Take Up Too Much Of Today.” – Will Rogers',
#     '“You Learn More From Failure Than From Success. Don’t Let It Stop You. Failure Builds Character.” – Unknown',
#     '“If You Are Working On Something That You Really Care About, You Don’t Have To Be Pushed. The Vision Pulls You.” – Steve Jobs',
# )


@app.route('/', methods=["GET", "POST"])
def load_page():
    search_query = ""
    if request.method == 'POST':
        search_query = request.form.get("search_query", None)

    def query_database(search_query):
        jdb = Jumbo()
        term = jdb.wikipedia.search("wikipedia_docs_full", query={"match": {"content": f"{search_query}"}})
        return term

    if search_query:
        search_query = query_database(search_query)
        print(search_query.keys())
        return render_template('website.html', search_query=search_query)
    return render_template('website.html')

    return render_template("website.html")


##############
# Exercise 1 #
##############
if __name__ == "__main__":
    app.debug = True
    app.run(port=5051)

#
# ##############
# # Exercise 2 #
# ##############
# @app.route('/<search_term>', methods=['GET'])
# def exercise2(search_term=''):
#     pprint(search_term)
#     return search_term
#
#
# ##############
# # Exercise 3 #
# ##############
# @app.route('/restaurant-data/<city>/<search_term>')
# @app.route('/restaurant-data/<city>')
# @app.route('/restaurant-data')
# def exercise3(city='' or 'Evanston, IL', search_term=''):
#     url = 'https://www.apitutor.org/yelp/simple/v3/businesses/search?location={0}&term={1}'.format(city, search_term)
#     response = requests.get(url)
#     data = response.json()
#     pprint(data) # for debugging -- prints the result to the command line
#     return json.dumps(data)
#
# ##############
# # Exercise 4 #
# ##############
# @app.route('/restaurant/<city>/<search_term>')
# @app.route('/restaurant/<city>')
# @app.route('/restaurant')
# def exercise4(city='Evanston, IL', search_term=''):
#     url = 'https://www.apitutor.org/yelp/simple/v3/businesses/search?location={0}&term={1}'.format(city, search_term)
#     response = requests.get(url)
#     restaurants = response.json()
#     pprint(restaurants[0]) # for debugging
#     return render_template(
#         'restaurant.html',
#         user=current_user,
#         search_term=search_term,
#         city=city,
#         restaurant=restaurants[0]
#     )
#
# @app.route('/cards')
# def photos_static():
#     return render_template('cards.html')
#
#
